from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models.identity import Identity
from models.risk import RiskScore
from models.transaction import Transaction
from schemas import (
    TransactionCreateRequest,
    TransactionResponse,
    TransactionRiskPredictRequest,
    TransactionRiskPredictResponse,
)
from services.ai_service import ai_service
from services.blockchain_service import blockchain_service
from services.transaction_service import transaction_service


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/predict-risk", response_model=TransactionRiskPredictResponse)
def predict_risk(payload: TransactionRiskPredictRequest, db: Session = Depends(get_db)):
    recent_cutoff = datetime.utcnow() - timedelta(hours=1)
    recent_txs = (
        db.query(Transaction)
        .filter(Transaction.sender == payload.sender, Transaction.created_at >= recent_cutoff)
        .all()
    )
    tx_count_last_hour, mean_interval_seconds = transaction_service.estimate_wallet_features(
        [tx.created_at for tx in recent_txs]
    )
    wallet_activity_ratio = min(1.0, tx_count_last_hour / 20.0)
    risk = ai_service.evaluate(
        payload.amount_eth, tx_count_last_hour, mean_interval_seconds, wallet_activity_ratio
    )
    return TransactionRiskPredictResponse(risk_score=risk.risk_score, anomaly_flag=risk.anomaly_flag)


@router.post("", response_model=TransactionResponse)
def create_transaction(payload: TransactionCreateRequest, db: Session = Depends(get_db)):
    identity = db.query(Identity).filter(Identity.eth_address == payload.sender).first()
    if not identity:
        raise HTTPException(status_code=404, detail="Sender identity not found.")

    recent_cutoff = datetime.utcnow() - timedelta(hours=1)
    recent_txs = (
        db.query(Transaction)
        .filter(Transaction.sender == payload.sender, Transaction.created_at >= recent_cutoff)
        .all()
    )
    tx_count_last_hour, mean_interval_seconds = transaction_service.estimate_wallet_features(
        [tx.created_at for tx in recent_txs]
    )
    wallet_activity_ratio = min(1.0, tx_count_last_hour / 20.0)
    risk = ai_service.evaluate(
        payload.amount_eth, tx_count_last_hour, mean_interval_seconds, wallet_activity_ratio
    )
    now = transaction_service.now_iso()
    metadata_hash = transaction_service.build_metadata_hash(
        payload.sender, payload.recipient, payload.amount_eth, now
    )
    pq_signature = transaction_service.sign_transaction_payload(
        {
            "sender": payload.sender,
            "recipient": payload.recipient,
            "amount_eth": payload.amount_eth,
            "eth_tx_hash": payload.eth_tx_hash,
            "metadata_hash": metadata_hash,
            "ts": now,
        },
        identity.encrypted_pq_private_key,
    )

    tx = Transaction(
        sender=payload.sender,
        recipient=payload.recipient,
        amount_eth=payload.amount_eth,
        eth_tx_hash=payload.eth_tx_hash,
        pq_signature=pq_signature,
        metadata_hash=metadata_hash,
        risk_score=risk.risk_score,
        anomaly_flag=risk.anomaly_flag,
    )
    db.add(tx)

    current_risk = db.query(RiskScore).filter(RiskScore.eth_address == payload.sender).first()
    if current_risk:
        current_risk.score = risk.risk_score
    else:
        db.add(RiskScore(eth_address=payload.sender, score=risk.risk_score))

    db.commit()
    blockchain_service.anchor_transaction(payload.eth_tx_hash, pq_signature, metadata_hash)
    blockchain_service.anchor_risk_score(payload.sender, risk.risk_score)

    return TransactionResponse(
        eth_tx_hash=payload.eth_tx_hash,
        metadata_hash=metadata_hash,
        pq_signature=pq_signature,
        risk_score=risk.risk_score,
        anomaly_flag=risk.anomaly_flag,
    )


@router.get("/{eth_address}")
def list_transactions(eth_address: str, db: Session = Depends(get_db)):
    txs = (
        db.query(Transaction)
        .filter(Transaction.sender == eth_address)
        .order_by(Transaction.created_at.desc())
        .limit(100)
        .all()
    )
    return [
        {
            "eth_tx_hash": tx.eth_tx_hash,
            "recipient": tx.recipient,
            "amount_eth": tx.amount_eth,
            "risk_score": tx.risk_score,
            "anomaly_flag": tx.anomaly_flag,
            "created_at": tx.created_at.isoformat(),
        }
        for tx in txs
    ]
