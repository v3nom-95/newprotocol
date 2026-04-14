from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.deps import require_roles
from db import get_db
from models.identity import Identity
from schemas import IdentityCreateRequest, IdentityResponse
from services.blockchain_service import blockchain_service
from services.wallet_service import wallet_service


router = APIRouter(prefix="/identity", tags=["identity"])


@router.post("", response_model=IdentityResponse)
def create_identity(
    payload: IdentityCreateRequest,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin", "service")),
):
    existing = db.query(Identity).filter(Identity.eth_address == payload.eth_address).first()
    if existing:
        raise HTTPException(status_code=409, detail="Identity already exists for this address.")

    material = wallet_service.create_identity_material(payload.eth_address)
    identity = Identity(
        eth_address=payload.eth_address,
        did=material["did"],
        did_hash=material["did_hash"],
        pq_public_key=material["pq_public_key"],
        encrypted_pq_private_key=material["encrypted_pq_private_key"],
        pq_algorithm=material["pq_algorithm"],
        key_version=int(material["key_version"]),
    )
    db.add(identity)
    db.commit()
    db.refresh(identity)
    identity_op_payload = {
        "eth_address": payload.eth_address.lower(),
        "did_hash": material["did_hash"],
    }
    operation_id = f"identity-{blockchain_service.hash_payload(identity_op_payload)}"
    blockchain_service.anchor_identity(db, operation_id, payload.eth_address, material["did_hash"])

    return IdentityResponse(
        eth_address=identity.eth_address,
        did=identity.did,
        did_hash=identity.did_hash,
        pq_public_key=identity.pq_public_key,
    )


@router.get("/{eth_address}", response_model=IdentityResponse)
def get_identity(
    eth_address: str,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin", "service", "user")),
):
    identity = db.query(Identity).filter(Identity.eth_address == eth_address).first()
    if not identity:
        raise HTTPException(status_code=404, detail="Identity not found.")
    return IdentityResponse(
        eth_address=identity.eth_address,
        did=identity.did,
        did_hash=identity.did_hash,
        pq_public_key=identity.pq_public_key,
    )
