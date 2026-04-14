from datetime import datetime

from pydantic import BaseModel, Field


class IdentityCreateRequest(BaseModel):
    eth_address: str = Field(min_length=42, max_length=64)


class IdentityResponse(BaseModel):
    eth_address: str
    did: str
    did_hash: str
    pq_public_key: str


class TransactionCreateRequest(BaseModel):
    sender: str
    recipient: str
    amount_eth: float = Field(gt=0)
    eth_tx_hash: str


class TransactionRiskPredictRequest(BaseModel):
    sender: str
    amount_eth: float = Field(gt=0)


class TransactionRiskPredictResponse(BaseModel):
    risk_score: float
    anomaly_flag: bool


class TransactionResponse(BaseModel):
    eth_tx_hash: str
    metadata_hash: str
    risk_score: float
    anomaly_flag: bool
    pq_signature: str


class RiskResponse(BaseModel):
    eth_address: str
    score: float


class HealthResponse(BaseModel):
    status: str
