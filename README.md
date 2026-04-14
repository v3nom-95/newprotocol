# Q-AI Chain Trust Protocol

Quantum-Secure AI-Powered Trust Protocol providing a modular stack for identity verification, fraud detection, and blockchain anchoring.

## 🚀 Quick Start

For detailed step-by-step instructions on deployment and local development, please refer to the [Setup Guide](SETUP_GUIDE.md).

## 📂 Project Structure

- `contracts/` - Solidity registries (Identity, Transactions, Risk)
- `backend/` - FastAPI protocol server with PQC integration
- `ai-engine/` - IsolationForest training and inference artifacts
- `frontend/` - React + Tailwind dashboard for protocol visualization
- `sdk/` - Developer SDK (ethers.js v6 + API clients)
- `infra/` - Docker Compose and Nginx configuration

---

## 🛠 Project Components

### Smart Contracts
Registries for decentralized identity and on-chain risk scoring.
- `IdentityRegistry.sol`: Manage user DIDs.
- `TransactionRegistry.sol`: Securely store PQC signed transactions.
- `RiskRegistry.sol`: Anchor risk scores on-chain.

### AI Engine
Fraud detection via an Isolation Forest anomaly detection model.
- Automatically trained to detect malicious patterns in protocol transactions.

### Backend Protocol
Unified API layer that coordinates AI scoring, authentication, and blockchain relay.
- Integrated with PQC (Post-Quantum Cryptography) for secure signatures.

### Frontend Dashboard
Real-time dashboard for managing identities and monitoring risk across the network.

### SDK
Simplify integration for external services to interact with the trust protocol.

---

## 🏗 High-Level Deployment

1. **Deploy Contracts**: Use Hardhat in the `contracts` folder.
2. **Environment Configuration**: Set `.env` files in `backend`, `contracts`, and `frontend`.
3. **Train AI Engine**: Run `training.py` in `ai-engine`.
4. **Run Services**: Start the backend and frontend locally or via `infra/` docker-compose.

---

## 🛡 Security & Design

- **Quantum Security**: PQ private keys are encrypted and stored securely.
- **Relayer Path**: Advanced relayer with nonce management and idempotency.
- **Modularity**: Components can be deployed independently as needed.

---

## 🤝 Contribution

This repository is optimized for the protocol's core functionality. Test files and build artifacts are excluded to maintain a clean protocol workspace.

