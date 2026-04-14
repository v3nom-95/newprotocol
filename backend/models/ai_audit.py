from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class AIAudit(Base):
    __tablename__ = "ai_audits"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    features_json: Mapped[str] = mapped_column(Text, nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    anomaly_flag: Mapped[bool] = mapped_column(Boolean, nullable=False)
    drift_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
