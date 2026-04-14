from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Iterable

from pqcrypto.dilithium import sign_payload, verify_signature
from utils.security import decrypt_secret
from config.settings import settings


class TransactionService:
    def build_metadata_hash(self, sender: str, recipient: str, amount_eth: float, ts: str) -> str:
        payload = f"{sender}:{recipient}:{amount_eth}:{ts}"
        return "0x" + sha256(payload.encode("utf-8")).hexdigest()

    def sign_transaction_payload(self, payload: dict, encrypted_private_key: str) -> str:
        private_key = decrypt_secret(encrypted_private_key, settings.aes_master_key)
        return sign_payload(payload, private_key)

    @staticmethod
    def verify_transaction_payload(payload: dict, signature: str, public_key: str) -> bool:
        raw = json.dumps(payload, sort_keys=True).encode("utf-8")
        return verify_signature(raw, signature, public_key)

    def estimate_wallet_features(self, recent_timestamps: Iterable[datetime]) -> tuple[int, float]:
        timestamps = sorted(recent_timestamps)
        tx_count = len(timestamps)
        if tx_count <= 1:
            return tx_count, 3600.0
        intervals = [(timestamps[i] - timestamps[i - 1]).total_seconds() for i in range(1, tx_count)]
        mean_interval = sum(intervals) / len(intervals)
        return tx_count, mean_interval

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()


transaction_service = TransactionService()
