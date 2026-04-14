# Q-AI Chain Production Architecture

## Runtime Components
- FastAPI backend with JWT auth, RBAC, and rate limits
- PostgreSQL for identities, transactions, risk, audit, and chain job tables
- Redis for risk caching and relayer idempotency cache
- Sepolia smart contracts for trust anchoring
- React dashboard for ops and user actions
- SDK for third-party integrations

## Security Controls
- AES encryption at rest for PQ private keys
- JWT access/refresh token model
- Role-based API gating for write operations
- Relayer nonce management and retry controls
- Metrics endpoint with optional token guard
