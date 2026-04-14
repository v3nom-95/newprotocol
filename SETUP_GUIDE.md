# Q-AI Chain Setup Guide

This guide provides step-by-step instructions for setting up and running the Q-AI Chain project in your local environment.

## 1. Prerequisites

Before you begin, ensure you have the following installed:
- **Node.js** (v18+) and **npm**
- **Python** (v3.9+)
- **Docker** and **Docker Compose**
- **Git**

---

## 2. Setting Up Environment Variables

The project uses `.env` files in multiple directories. You must copy the `.env.example` files and fill in the required values.

### Backend `.env` (`backend/.env`)
Key variables:
- `DATABASE_URL`: Connection string for PostgreSQL.
- `REDIS_URL`: Connection string for Redis.
- `RPC_URL`: Your Ethereum RPC endpoint (e.g., Infura/Alchemy for Sepolia).
- `RELAYER_PRIVATE_KEY`: Private key for the account that will anchor transactions on-chain.
- `JWT_SECRET`: A strong secret for signing auth tokens.
- `IDENTITY_REGISTRY_ADDRESS`, `TX_REGISTRY_ADDRESS`, `RISK_REGISTRY_ADDRESS`: Addresses of the deployed smart contracts.

### Smart Contracts `.env` (`contracts/.env`)
Key variables:
- `SEPOLIA_URL`: Your Ethereum RPC endpoint.
- `PRIVATE_KEY`: The deployer account private key.
- `ETHERSCAN_API_KEY`: Required if you want to verify your contracts.

### Frontend `.env` (`frontend/.env`)
Key variables:
- `VITE_API_BASE_URL`: The URL of your backend API (default: `http://localhost:8000/api/v1`).

---

## 3. Smart Contract Deployment

1. Navigate to the `contracts` directory:
   ```bash
   cd contracts
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Compile the contracts:
   ```bash
   npx hardhat compile
   ```
4. Deploy to Sepolia (or your preferred network):
   ```bash
   npx hardhat run scripts/deploy.js --network sepolia
   ```
5. **Important**: Copy the deployed addresses from the terminal output and paste them into your `backend/.env` file.

---

## 4. AI Engine Setup

1. Navigate to the `ai-engine` directory:
   ```bash
   cd ai-engine
   ```
2. Install dependencies (it's recommended to use a virtual environment):
   ```bash
   pip install -r ../backend/requirements.txt
   ```
3. Train the initial model and generate artifacts:
   ```bash
   python training.py
   ```
   This will create `artifacts/isolation_forest.joblib` and `artifacts/scaler.joblib`.

---

## 5. Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run database migrations using Alembic:
   ```bash
   alembic upgrade head
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

---

## 6. Frontend Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The dashboard should now be available at `http://localhost:5173`.

---

## 7. Running with Docker (Recommended)

To run the entire stack (PostgreSQL, Redis, Backend, and Frontend) using Docker:

1. Navigate to the `infra` directory:
   ```bash
   cd infra
   ```
2. Start the services:
   ```bash
   docker compose up -d
   ```
3. For a production-like build behind Nginx:
   ```bash
   docker compose -f docker-compose.prod.yml up -d --build
   ```

---

## 8. Development Order of Operations

1. **Deploy Contracts**: Get addresses first.
2. **Update Backend ENV**: Add addresses and secrets.
3. **Train AI Engine**: Ensure artifacts exist.
4. **Start Backend**: Handle DB migrations and API server.
5. **Start Frontend**: Launch the dashboard.
