import { useEffect } from "react";
import { useProtocolStore } from "../store/useProtocolStore";

export default function DashboardPage() {
  const { currentAddress, riskScore, transactions, fetchRisk, fetchTransactions } = useProtocolStore();

  useEffect(() => {
    if (currentAddress) {
      fetchRisk(currentAddress);
      fetchTransactions(currentAddress);
    }
  }, [currentAddress, fetchRisk, fetchTransactions]);

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Dashboard</h2>
      <div className="rounded border border-slate-800 p-4">Wallet: {currentAddress || "Not selected"}</div>
      <div className="rounded border border-slate-800 p-4">Risk Score: {riskScore.toFixed(2)}</div>
      <div className="rounded border border-slate-800 p-4">
        <h3 className="mb-2 font-medium">Recent Transactions</h3>
        <ul className="space-y-1 text-sm">
          {transactions.slice(0, 5).map((tx) => (
            <li key={tx.eth_tx_hash}>{tx.eth_tx_hash} | {tx.amount_eth} ETH | Risk {tx.risk_score?.toFixed?.(2) ?? tx.risk_score}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
