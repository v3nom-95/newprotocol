import hashlib
import json
from typing import Any


class BlockchainService:
    """
    MVP anchor service.
    In production, replace stubs with web3/ethers relayer calls.
    """

    @staticmethod
    def hash_payload(payload: dict[str, Any]) -> str:
        raw = json.dumps(payload, sort_keys=True).encode("utf-8")
        return "0x" + hashlib.sha256(raw).hexdigest()

    def anchor_identity(self, eth_address: str, did_hash: str) -> dict[str, str]:
        return {"status": "anchored", "eth_address": eth_address, "did_hash": did_hash}

    def anchor_transaction(self, tx_hash: str, pq_signature: str, metadata_hash: str) -> dict[str, str]:
        return {
            "status": "anchored",
            "tx_hash": tx_hash,
            "pq_signature_prefix": pq_signature[:16],
            "metadata_hash": metadata_hash,
        }

    def anchor_risk_score(self, eth_address: str, score: float) -> dict[str, str]:
        score_hash = self.hash_payload({"eth_address": eth_address, "score": score})
        return {"status": "anchored", "eth_address": eth_address, "score_hash": score_hash}


blockchain_service = BlockchainService()
