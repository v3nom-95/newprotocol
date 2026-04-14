from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models.identity import Identity
from schemas import IdentityCreateRequest, IdentityResponse
from services.blockchain_service import blockchain_service
from services.wallet_service import wallet_service


router = APIRouter(prefix="/identity", tags=["identity"])


@router.post("", response_model=IdentityResponse)
def create_identity(payload: IdentityCreateRequest, db: Session = Depends(get_db)):
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
    )
    db.add(identity)
    db.commit()
    db.refresh(identity)
    blockchain_service.anchor_identity(payload.eth_address, material["did_hash"])

    return IdentityResponse(
        eth_address=identity.eth_address,
        did=identity.did,
        did_hash=identity.did_hash,
        pq_public_key=identity.pq_public_key,
    )


@router.get("/{eth_address}", response_model=IdentityResponse)
def get_identity(eth_address: str, db: Session = Depends(get_db)):
    identity = db.query(Identity).filter(Identity.eth_address == eth_address).first()
    if not identity:
        raise HTTPException(status_code=404, detail="Identity not found.")
    return IdentityResponse(
        eth_address=identity.eth_address,
        did=identity.did,
        did_hash=identity.did_hash,
        pq_public_key=identity.pq_public_key,
    )
