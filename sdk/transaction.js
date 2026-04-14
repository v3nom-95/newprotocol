import { ethers } from "ethers";
import axios from "axios";

const API_URL = process.env.QAI_API_URL || "http://localhost:8000/api/v1";

export async function sendTransaction({
  rpcUrl,
  privateKey,
  to,
  amountEth,
}) {
  const provider = new ethers.JsonRpcProvider(rpcUrl);
  const wallet = new ethers.Wallet(privateKey, provider);
  const tx = await wallet.sendTransaction({
    to,
    value: ethers.parseEther(String(amountEth)),
  });
  await tx.wait();
  const record = await axios.post(`${API_URL}/transactions`, {
    sender: wallet.address,
    recipient: to,
    amount_eth: Number(amountEth),
    eth_tx_hash: tx.hash,
  });
  return { chainTx: tx.hash, protocolRecord: record.data };
}

export async function getTransactions(address) {
  const { data } = await axios.get(`${API_URL}/transactions/${address}`);
  return data;
}
