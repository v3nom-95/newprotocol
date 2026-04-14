import hashlib
import json
import time
from typing import Any

from sqlalchemy.exc import IntegrityError
from web3 import Web3
from web3.exceptions import TimeExhausted, TransactionNotFound

from blockchain.abis import IDENTITY_REGISTRY_ABI, RISK_REGISTRY_ABI, TRANSACTION_REGISTRY_ABI
from config.settings import settings
from models.chain_job import ChainJob
from services.cache_service import cache_service


class BlockchainService:
    def __init__(self) -> None:
        self.w3 = Web3(Web3.HTTPProvider(settings.rpc_url))
        self.enabled = bool(settings.relayer_private_key) and self.w3.is_connected()
        self.account = None
        if self.enabled:
            self.account = self.w3.eth.account.from_key(settings.relayer_private_key)

    @staticmethod
    def hash_payload(payload: dict[str, Any]) -> str:
        raw = json.dumps(payload, sort_keys=True).encode("utf-8")
        return "0x" + hashlib.sha256(raw).hexdigest()

    def _record_job(self, db, operation_id: str, job_type: str) -> ChainJob:
        job = db.query(ChainJob).filter(ChainJob.operation_id == operation_id).first()
        if job:
            return job

        job = ChainJob(operation_id=operation_id, job_type=job_type, status="pending", attempts=0)
        db.add(job)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            job = db.query(ChainJob).filter(ChainJob.operation_id == operation_id).first()
            if job:
                return job
            raise

        db.refresh(job)
        return job

    def _resolve_existing_job(self, db, job: ChainJob, cache_key: str) -> dict[str, str] | None:
        if job.status == "anchored" and job.tx_hash:
            return {"status": "anchored", "tx_hash": job.tx_hash}

        if not job.tx_hash:
            return None

        try:
            receipt = self.w3.eth.get_transaction_receipt(job.tx_hash)
            if receipt and receipt.status == 1:
                job.status = "anchored"
                job.last_error = ""
                db.commit()
                result = {"status": "anchored", "tx_hash": job.tx_hash}
                cache_service.set_json(cache_key, result, 3600)
                return result
            if receipt:
                job.status = "dead_letter"
                job.last_error = "transaction failed on-chain"
                db.commit()
                return {"status": "dead_letter", "reason": "transaction failed on-chain"}
        except TransactionNotFound:
            return {"status": "pending", "tx_hash": job.tx_hash}

        return None

    def _send_contract_tx(
        self,
        db,
        operation_id: str,
        contract_address: str,
        abi: list[dict],
        fn_name: str,
        args: list[Any],
        job_type: str,
    ) -> dict[str, str]:
        cache_key = f"chain:op:{operation_id}"
        cached = cache_service.get_json(cache_key)
        if cached:
            return cached

        job = self._record_job(db, operation_id, job_type)
        resolved = self._resolve_existing_job(db, job, cache_key)
        if resolved:
            return resolved

        if not self.enabled or self.account is None:
            result = {"status": "simulated", "reason": "relayer-not-configured"}
            cache_service.set_json(cache_key, result, 60)
            return result

        contract = self.w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
        last_error = ""
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                tx_fn = getattr(contract.functions, fn_name)(*args)
                nonce = self.w3.eth.get_transaction_count(self.account.address, block_identifier="pending")
                tx = tx_fn.build_transaction(
                    {
                        "from": self.account.address,
                        "nonce": nonce,
                        "gas": 400000,
                        "gasPrice": self.w3.eth.gas_price,
                        "chainId": self.w3.eth.chain_id,
                    }
                )
                signed = self.account.sign_transaction(tx)
                raw_tx = signed.raw_transaction
                tx_hash = self.w3.eth.send_raw_transaction(raw_tx)
                tx_hash_hex = tx_hash.hex()

                job.status = "retrying"
                job.tx_hash = tx_hash_hex
                job.attempts = attempt
                job.last_error = ""
                db.commit()

                try:
                    receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
                    if receipt.status == 1:
                        result = {"status": "anchored", "tx_hash": tx_hash_hex}
                        job.status = "anchored"
                        job.last_error = ""
                        job.tx_hash = tx_hash_hex
                        db.commit()
                        cache_service.set_json(cache_key, result, 3600)
                        return result
                    job.status = "dead_letter"
                    job.last_error = "transaction rolled back on-chain"
                    db.commit()
                    return {"status": "dead_letter", "reason": "transaction rolled back on-chain"}
                except TimeExhausted:
                    return {"status": "pending", "tx_hash": tx_hash_hex}

            except Exception as exc:
                last_error = str(exc)
                job.status = "retrying"
                job.attempts = attempt
                job.last_error = last_error
                db.commit()
                if attempt == max_attempts:
                    job.status = "dead_letter"
                    db.commit()
                    return {"status": "dead_letter", "reason": last_error}
                time.sleep(attempt)

        job.status = "dead_letter"
        job.last_error = last_error
        db.commit()
        return {"status": "dead_letter", "reason": last_error}

    def anchor_identity(self, db, operation_id: str, eth_address: str, did_hash: str) -> dict[str, str]:
        if settings.identity_registry_address.lower() == "0x0000000000000000000000000000000000000000":
            return {"status": "simulated", "eth_address": eth_address, "did_hash": did_hash}
        return self._send_contract_tx(
            db,
            operation_id,
            settings.identity_registry_address,
            IDENTITY_REGISTRY_ABI,
            "registerIdentity",
            [Web3.to_checksum_address(eth_address), did_hash],
            "identity",
        )

    def anchor_transaction(
        self, db, operation_id: str, tx_hash: str, pq_signature: str, metadata_hash: str
    ) -> dict[str, str]:
        if settings.tx_registry_address.lower() == "0x0000000000000000000000000000000000000000":
            return {"status": "simulated", "tx_hash": tx_hash, "metadata_hash": metadata_hash}
        tx_hash_bytes32 = bytes.fromhex(tx_hash[2:].rjust(64, "0"))
        metadata_hash_bytes32 = bytes.fromhex(metadata_hash[2:].rjust(64, "0"))
        signature_bytes = pq_signature.encode("utf-8")
        return self._send_contract_tx(
            db,
            operation_id,
            settings.tx_registry_address,
            TRANSACTION_REGISTRY_ABI,
            "storeTransaction",
            [tx_hash_bytes32, signature_bytes, metadata_hash_bytes32],
            "transaction",
        )

    def anchor_risk_score(self, db, operation_id: str, eth_address: str, score: float) -> dict[str, str]:
        if settings.risk_registry_address.lower() == "0x0000000000000000000000000000000000000000":
            score_hash = self.hash_payload({"eth_address": eth_address, "score": score})
            return {"status": "simulated", "eth_address": eth_address, "score_hash": score_hash}
        return self._send_contract_tx(
            db,
            operation_id,
            settings.risk_registry_address,
            RISK_REGISTRY_ABI,
            "storeRiskScore",
            [Web3.to_checksum_address(eth_address), int(score)],
            "risk",
        )


blockchain_service = BlockchainService()
