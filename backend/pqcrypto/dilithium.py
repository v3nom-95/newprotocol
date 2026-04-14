import base64
import hashlib
import hmac
import json
from typing import Dict


def _try_oqs():
    try:
        import oqs  # type: ignore

        return oqs
    except Exception:
        return None


def generate_keypair() -> Dict[str, str]:
    oqs = _try_oqs()
    if oqs:
        with oqs.Signature("Dilithium2") as signer:
            public_key = signer.generate_keypair()
            secret_key = signer.export_secret_key()
            return {
                "public_key": base64.b64encode(public_key).decode(),
                "private_key": base64.b64encode(secret_key).decode(),
            }

    seed = hashlib.sha256(b"qai-dev-dilithium-fallback").digest()
    return {
        "public_key": base64.b64encode(seed).decode(),
        "private_key": base64.b64encode(seed).decode(),
    }


def sign_data(data: bytes, private_key: str) -> str:
    oqs = _try_oqs()
    key_bytes = base64.b64decode(private_key.encode())
    if oqs:
        with oqs.Signature("Dilithium2", secret_key=key_bytes) as signer:
            signature = signer.sign(data)
            return base64.b64encode(signature).decode()
    digest = hmac.new(key_bytes, data, hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def verify_signature(data: bytes, signature: str, public_key: str) -> bool:
    oqs = _try_oqs()
    sig_bytes = base64.b64decode(signature.encode())
    key_bytes = base64.b64decode(public_key.encode())
    if oqs:
        with oqs.Signature("Dilithium2") as verifier:
            return verifier.verify(data, sig_bytes, key_bytes)
    expected = hmac.new(key_bytes, data, hashlib.sha256).digest()
    return hmac.compare_digest(expected, sig_bytes)


def sign_payload(payload: dict, private_key: str) -> str:
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    return sign_data(raw, private_key)
