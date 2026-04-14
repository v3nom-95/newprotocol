from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sender: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    recipient: Mapped[str] = mapped_column(String(64), nullable=False)
    amount_eth: Mapped[float] = mapped_column(Float, nullable=False)
    eth_tx_hash: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    pq_signature: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_hash: Mapped[str] = mapped_column(String(80), nullable=False)
    anomaly_flag: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
