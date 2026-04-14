# Release Checklist

- Confirm Sepolia contracts are deployed and addresses set in `backend/.env`.
- Run DB migrations: `cd backend && alembic upgrade head`.
- Run backend test suite: `cd backend && pytest -q`.
- Run contract tests: `cd contracts && npm install && npm test`.
- Run frontend build: `cd frontend && npm ci && npm run build`.
- Confirm `/metrics` endpoint availability with `METRICS_TOKEN`.
- Validate auth flow (`/auth/login`, protected write APIs).
- Verify relayer dead-letter queue is empty in `chain_jobs`.
- Tag release and store deployment artifact manifest.
