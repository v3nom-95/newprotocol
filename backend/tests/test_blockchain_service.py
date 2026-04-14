from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import Base
from services.blockchain_service import blockchain_service


def test_hash_payload_is_deterministic():
    payload_a = {"b": 2, "a": 1}
    payload_b = {"a": 1, "b": 2}
    assert blockchain_service.hash_payload(payload_a) == blockchain_service.hash_payload(payload_b)


def test_record_job_reuses_existing_operation_id():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    blockchain_service.enabled = False
    op_id = "test-operation-retry"
    job1 = blockchain_service._record_job(db, op_id, "transaction")
    job2 = blockchain_service._record_job(db, op_id, "transaction")

    assert job1.id == job2.id
    assert job1.operation_id == op_id
    assert job2.operation_id == op_id


def test_anchor_identity_returns_simulated_when_relayer_disabled():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    blockchain_service.enabled = False
    result = blockchain_service.anchor_identity(db, "sim-op", "0x1234567890abcdef1234567890abcdef12345678", "0xdeadbeef")

    assert result["status"] == "simulated"
    assert result["reason"] == "relayer-not-configured"
