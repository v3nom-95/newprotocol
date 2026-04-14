# Q-AI Chain

Quantum-Secure AI-Powered Trust Protocol with modular layers:
- Q-DID identity (PQ + Ethereum)
- AI fraud scoring
- Blockchain anchoring contracts
- FastAPI backend
- React dashboard
- JavaScript SDK

## Project Structure

`contracts/` Solidity registries  
`backend/` FastAPI protocol server  
`ai-engine/` IsolationForest training + inference model  
`frontend/` React + Tailwind dashboard  
`sdk/` Developer SDK (ethers.js v6 + API clients)  
`infra/` Docker Compose + optional Nginx

## Smart Contracts

- `IdentityRegistry.sol`
  - `registerIdentity(address user, bytes32 didHash)`
  - `getIdentity(address user)`
- `TransactionRegistry.sol`
  - `storeTransaction(bytes32 txHash, bytes pqSignature, bytes32 metadataHash)`
- `RiskRegistry.sol`
  - `storeRiskScore(address user, uint256 score)`
  - `getRiskScore(address user)`

Deploy to Sepolia using your preferred toolchain (Hardhat/Foundry/Remix), then place deployed addresses in `backend/.env`.
To enable live on-chain anchoring from the API, also set `RELAYER_PRIVATE_KEY` in backend env.

## Backend Setup

1. Copy env:
   - `backend/.env.example` -> `backend/.env`
2. Install:
   - `cd backend`
   - `python -m pip install -r requirements.txt`
3. Train AI model:
   - `cd ../ai-engine`
   - `python training.py`
4. Run API:
   - `cd ../backend`
   - `uvicorn main:app --reload --host 0.0.0.0 --port 8000`

API base: `http://localhost:8000/api/v1`

Key endpoints:
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /identity` (role: `admin|service`)
- `GET /identity/{eth_address}` (role: `admin|service|user`)
- `POST /transactions/predict-risk`
- `POST /transactions` (role: `admin|service`)
- `GET /transactions/{eth_address}`
- `GET /risk/{eth_address}`
- `GET /metrics?token=...`

Default local users for development:
- `admin@qai.local` / `Admin@123`
- `service@qai.local` / `Service@123`
- `user@qai.local` / `User@123`

## Frontend Setup

1. `cd frontend`
2. `npm install`
3. Copy `.env.example` to `.env` if needed
4. `npm run dev`

Pages included:
- Dashboard
- Identity
- Send Transaction
- Transaction Explorer
- Admin Panel

## SDK Setup

1. `cd sdk`
2. `npm install`

Exports:
- `createWallet()`
- `sendTransaction()`
- `getRiskScore()`
- `getTransactions()`

Example:

```js
import { createWallet, sendTransaction, getRiskScore } from "qai-chain-sdk";
```

## Docker Setup (Development)

From `infra/`:

```bash
docker compose up -d
```

Services:
- PostgreSQL: `5432`
- Redis: `6379`
- Backend: `8000`
- Frontend: `5173`

## Docker Setup (Production-like)

From `infra/`:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

This profile runs backend/frontend containers behind Nginx on port `80`.

## Database Migrations

```bash
cd backend
alembic upgrade head
```

## Security Notes

- PQ private keys are AES-encrypted before DB storage.
- Backend enforces request rate limits, JWT auth, and RBAC on protected endpoints.
- Inputs are validated with Pydantic schemas.
- Relayer path uses retries, nonce-from-pending, idempotency cache, and dead-letter status tracking.
- Never commit real secrets to source control.

## Testing

- Backend: `cd backend && pytest -q`
- Frontend build: `cd frontend && npm run build`
- Contracts: `cd contracts && npm install && npm test`
- Load baseline: `k6 run tests/load/transactions.js`

## Production Runbooks

- Release checklist: `docs/release-checklist.md`
- Rollback runbook: `docs/rollback-runbook.md`
- Architecture notes: `docs/architecture.md`
