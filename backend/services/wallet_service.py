import hashlib

from config.settings import settings
from pqcrypto.dilithium import generate_keypair
from utils.security import encrypt_secret


class WalletService:
    @staticmethod
    def create_did(eth_address: str) -> str:
        return f"did:qai:{eth_address.lower()}"

    @staticmethod
    def create_identity_material(eth_address: str) -> dict[str, str]:
        keys = generate_keypair()
        did = WalletService.create_did(eth_address)
        did_hash = "0x" + hashlib.sha256(did.encode("utf-8")).hexdigest()
        encrypted_private = encrypt_secret(keys["private_key"], settings.aes_master_key)
        return {
            "did": did,
            "did_hash": did_hash,
            "pq_public_key": keys["public_key"],
            "encrypted_pq_private_key": encrypted_private,
        }


wallet_service = WalletService()
