import { ethers } from "ethers";
import axios from "axios";
import { QAIError } from "./errors.js";

const API_URL = process.env.QAI_API_URL || "http://localhost:8000/api/v1";

async function withRetry(fn, retries = 3) {
  let lastErr;
  for (let attempt = 1; attempt <= retries; attempt += 1) {
    try {
      return await fn();
    } catch (err) {
      lastErr = err;
      await new Promise((resolve) => setTimeout(resolve, attempt * 500));
    }
  }
  throw lastErr;
}

export async function sendTransaction({
  rpcUrl,
  privateKey,
  to,
  amountEth,
}) {
  const provider = new ethers.JsonRpcProvider(rpcUrl);
  const wallet = new ethers.Wallet(privateKey, provider);
  try {
    const tx = await withRetry(() =>
      wallet.sendTransaction({
        to,
        value: ethers.parseEther(String(amountEth)),
      })
    );
    await tx.wait();
    const record = await withRetry(() =>
      axios.post(`${API_URL}/transactions`, {
        sender: wallet.address,
        recipient: to,
        amount_eth: Number(amountEth),
        eth_tx_hash: tx.hash,
      })
    );
    return { chainTx: tx.hash, protocolRecord: record.data };
  } catch (err) {
    throw new QAIError("TX_SUBMIT_FAILED", "Failed to submit transaction", err?.response?.data || err?.message);
  }
}

export async function getTransactions(address, page = 1, pageSize = 50) {
  const { data } = await axios.get(`${API_URL}/transactions/${address}`, {
    params: { page, page_size: pageSize },
  });
  return data;
}
