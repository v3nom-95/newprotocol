from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Q-AI Chain API"
    environment: str = "dev"
    database_url: str = "postgresql+psycopg://qai:qai@postgres:5432/qai_chain"
    redis_url: str = "redis://redis:6379/0"
    model_path: str = "../ai-engine/artifacts/isolation_forest.joblib"
    feature_scaler_path: str = "../ai-engine/artifacts/scaler.joblib"
    aes_master_key: str = "change-me-in-env"
    rpc_url: str = "https://sepolia.infura.io/v3/your-key"
    relayer_private_key: str = ""
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_access_token_exp_minutes: int = 30
    jwt_refresh_token_exp_days: int = 7
    production_mode: bool = False
    ai_drift_threshold: float = 2.5
    risk_cache_ttl_seconds: int = 300
    log_level: str = "INFO"
    metrics_token: str = ""
    identity_registry_address: str = "0x0000000000000000000000000000000000000000"
    tx_registry_address: str = "0x0000000000000000000000000000000000000000"
    risk_registry_address: str = "0x0000000000000000000000000000000000000000"
    cors_origins: str = "http://localhost:5173"
    rate_limit: str = "120/minute"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
