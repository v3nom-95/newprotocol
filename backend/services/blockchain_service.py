import hashlib
import json
from typing import Any

from web3 import Web3

from blockchain.abis import IDENTITY_REGISTRY_ABI, RISK_REGISTRY_ABI, TRANSACTION_REGISTRY_ABI
from config.settings import settings


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

    def _send_contract_tx(self, contract_address: str, abi: list[dict], fn_name: str, args: list[Any]) -> dict[str, str]:
        if not self.enabled or self.account is None:
            return {"status": "simulated", "reason": "relayer-not-configured"}
        contract = self.w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
        tx_fn = getattr(contract.functions, fn_name)(*args)
        nonce = self.w3.eth.get_transaction_count(self.account.address)
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
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        return {"status": "anchored", "tx_hash": receipt.transactionHash.hex()}

    def anchor_identity(self, eth_address: str, did_hash: str) -> dict[str, str]:
        if settings.identity_registry_address.lower() == "0x0000000000000000000000000000000000000000":
            return {"status": "simulated", "eth_address": eth_address, "did_hash": did_hash}
        return self._send_contract_tx(
            settings.identity_registry_address,
            IDENTITY_REGISTRY_ABI,
            "registerIdentity",
            [Web3.to_checksum_address(eth_address), did_hash],
        )

    def anchor_transaction(self, tx_hash: str, pq_signature: str, metadata_hash: str) -> dict[str, str]:
        if settings.tx_registry_address.lower() == "0x0000000000000000000000000000000000000000":
            return {"status": "simulated", "tx_hash": tx_hash, "metadata_hash": metadata_hash}
        tx_hash_bytes32 = bytes.fromhex(tx_hash[2:].rjust(64, "0"))
        metadata_hash_bytes32 = bytes.fromhex(metadata_hash[2:].rjust(64, "0"))
        signature_bytes = pq_signature.encode("utf-8")
        return self._send_contract_tx(
            settings.tx_registry_address,
            TRANSACTION_REGISTRY_ABI,
            "storeTransaction",
            [tx_hash_bytes32, signature_bytes, metadata_hash_bytes32],
        )

    def anchor_risk_score(self, eth_address: str, score: float) -> dict[str, str]:
        if settings.risk_registry_address.lower() == "0x0000000000000000000000000000000000000000":
            score_hash = self.hash_payload({"eth_address": eth_address, "score": score})
            return {"status": "simulated", "eth_address": eth_address, "score_hash": score_hash}
        return self._send_contract_tx(
            settings.risk_registry_address,
            RISK_REGISTRY_ABI,
            "storeRiskScore",
            [Web3.to_checksum_address(eth_address), int(score)],
        )


blockchain_service = BlockchainService()
