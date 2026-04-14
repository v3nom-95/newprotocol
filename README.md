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
- `POST /identity`
- `GET /identity/{eth_address}`
- `POST /transactions`
- `GET /transactions/{eth_address}`
- `GET /risk/{eth_address}`

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

## Docker Setup

From `infra/`:

```bash
docker compose up -d
```

Services:
- PostgreSQL: `5432`
- Redis: `6379`
- Backend: `8000`
- Frontend: `5173`

## Security Notes

- PQ private keys are AES-encrypted before DB storage.
- Backend enforces request rate limits.
- Inputs are validated with Pydantic schemas.
- Never commit real secrets to source control.

## Current Scope (MVP)

This implementation provides a working protocol scaffold and end-to-end flow:
1. Create identity
2. Generate/store PQ keys
3. Anchor identity hash
4. Submit transaction metadata + PQ signature
5. Compute AI risk score
6. Persist/anchor risk
7. Visualize in dashboard

Next recommended steps:
- Replace blockchain anchor stubs with live contract calls.
- Integrate real `oqs-python` runtime for Dilithium/Kyber in production containers.
- Add auth, audit logging, and automated tests.
