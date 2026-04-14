import { ethers } from "ethers";
import axios from "axios";

const API_URL = process.env.QAI_API_URL || "http://localhost:8000/api/v1";

export async function createWallet() {
  const wallet = ethers.Wallet.createRandom();
  const identity = await axios.post(`${API_URL}/identity`, {
    eth_address: wallet.address,
  });
  return {
    address: wallet.address,
    privateKey: wallet.privateKey,
    did: identity.data.did,
    pqPublicKey: identity.data.pq_public_key,
  };
}
