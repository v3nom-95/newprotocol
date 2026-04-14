from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Identity(Base):
    __tablename__ = "identities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    eth_address: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    did: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    did_hash: Mapped[str] = mapped_column(String(66), nullable=False)
    pq_public_key: Mapped[str] = mapped_column(Text, nullable=False)
    encrypted_pq_private_key: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
