"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-04-14
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "identities",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("eth_address", sa.String(length=64), nullable=False),
        sa.Column("did", sa.String(length=255), nullable=False),
        sa.Column("did_hash", sa.String(length=66), nullable=False),
        sa.Column("pq_public_key", sa.Text(), nullable=False),
        sa.Column("encrypted_pq_private_key", sa.Text(), nullable=False),
        sa.Column("pq_algorithm", sa.String(length=32), nullable=False),
        sa.Column("key_version", sa.Integer(), nullable=False),
        sa.Column("rotated_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("eth_address"),
        sa.UniqueConstraint("did"),
    )
    op.create_index("ix_identities_eth_address", "identities", ["eth_address"], unique=False)

    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("sender", sa.String(length=64), nullable=False),
        sa.Column("recipient", sa.String(length=64), nullable=False),
        sa.Column("amount_eth", sa.Float(), nullable=False),
        sa.Column("eth_tx_hash", sa.String(length=80), nullable=False),
        sa.Column("pq_signature", sa.Text(), nullable=False),
        sa.Column("metadata_hash", sa.String(length=80), nullable=False),
        sa.Column("anomaly_flag", sa.Boolean(), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("eth_tx_hash"),
    )
    op.create_index("ix_transactions_sender", "transactions", ["sender"], unique=False)

    op.create_table(
        "risk_scores",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("eth_address", sa.String(length=64), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("eth_address"),
    )
    op.create_index("ix_risk_scores_eth_address", "risk_scores", ["eth_address"], unique=False)

    op.create_table(
        "chain_jobs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("operation_id", sa.String(length=128), nullable=False),
        sa.Column("job_type", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("last_error", sa.Text(), nullable=False),
        sa.Column("tx_hash", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("operation_id"),
    )
    op.create_index("ix_chain_jobs_operation_id", "chain_jobs", ["operation_id"], unique=False)

    op.create_table(
        "ai_audits",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("features_json", sa.Text(), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("anomaly_flag", sa.Boolean(), nullable=False),
        sa.Column("drift_score", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("ai_audits")
    op.drop_index("ix_chain_jobs_operation_id", table_name="chain_jobs")
    op.drop_table("chain_jobs")
    op.drop_index("ix_risk_scores_eth_address", table_name="risk_scores")
    op.drop_table("risk_scores")
    op.drop_index("ix_transactions_sender", table_name="transactions")
    op.drop_table("transactions")
    op.drop_index("ix_identities_eth_address", table_name="identities")
    op.drop_table("identities")
