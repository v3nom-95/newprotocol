import json

from pqcrypto.dilithium import generate_keypair, sign_data, verify_signature


def test_sign_and_verify_roundtrip():
    keys = generate_keypair()
    payload = json.dumps({"hello": "world"}, sort_keys=True).encode("utf-8")
    signature = sign_data(payload, keys["private_key"])
    assert verify_signature(payload, signature, keys["public_key"]) is True
