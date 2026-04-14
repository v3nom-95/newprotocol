from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models.risk import RiskScore
from schemas import RiskResponse


router = APIRouter(prefix="/risk", tags=["risk"])


@router.get("/{eth_address}", response_model=RiskResponse)
def get_risk(eth_address: str, db: Session = Depends(get_db)):
    risk = db.query(RiskScore).filter(RiskScore.eth_address == eth_address).first()
    if not risk:
        raise HTTPException(status_code=404, detail="Risk score not found.")
    return RiskResponse(eth_address=eth_address, score=risk.score)
