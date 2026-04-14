import base64
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
        with oqs.KeyEncapsulation("Kyber512") as kem:
            public_key = kem.generate_keypair()
            secret_key = kem.export_secret_key()
            return {
                "public_key": base64.b64encode(public_key).decode(),
                "private_key": base64.b64encode(secret_key).decode(),
            }
    return {"public_key": "", "private_key": ""}


def encapsulate(public_key: str) -> Dict[str, str]:
    oqs = _try_oqs()
    if not oqs:
        return {"ciphertext": "", "shared_secret": ""}
    with oqs.KeyEncapsulation("Kyber512") as kem:
        ciphertext, shared_secret = kem.encap_secret(base64.b64decode(public_key))
        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "shared_secret": base64.b64encode(shared_secret).decode(),
        }


def decapsulate(ciphertext: str, private_key: str) -> str:
    oqs = _try_oqs()
    if not oqs:
        return ""
    with oqs.KeyEncapsulation("Kyber512", secret_key=base64.b64decode(private_key)) as kem:
        shared_secret = kem.decap_secret(base64.b64decode(ciphertext))
        return base64.b64encode(shared_secret).decode()
