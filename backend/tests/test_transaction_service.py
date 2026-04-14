import json

from pqcrypto.dilithium import generate_keypair
from services.transaction_service import transaction_service
from utils.security import encrypt_secret


def test_transaction_payload_sign_and_verify_roundtrip():
    keys = generate_keypair()
    encrypted_private_key = encrypt_secret(keys["private_key"], "test-master-key")
    payload = {
        "sender": "0x1234567890abcdef",
        "recipient": "0xfedcba0987654321",
        "amount_eth": 1.234,
        "eth_tx_hash": "0x" + "a" * 64,
        "metadata_hash": "0x" + "b" * 64,
        "ts": "2026-04-14T12:00:00Z",
    }

    signature = transaction_service.sign_transaction_payload(payload, encrypted_private_key)
    assert isinstance(signature, str)
    assert transaction_service.verify_transaction_payload(payload, signature, keys["public_key"])
