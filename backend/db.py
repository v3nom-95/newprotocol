from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import settings
from models.base import Base
from models.ai_audit import AIAudit  # noqa: F401
from models.chain_job import ChainJob  # noqa: F401
from models.identity import Identity  # noqa: F401
from models.risk import RiskScore  # noqa: F401
from models.transaction import Transaction  # noqa: F401


engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
