import { useProtocolStore } from "../store/useProtocolStore";

export default function ExplorerPage() {
  const { transactions } = useProtocolStore();
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Transaction Explorer</h2>
      <div className="overflow-x-auto rounded border border-slate-800">
        <table className="w-full text-sm">
          <thead className="bg-slate-900">
            <tr>
              <th className="p-2 text-left">Hash</th>
              <th className="p-2 text-left">Amount</th>
              <th className="p-2 text-left">Risk</th>
              <th className="p-2 text-left">Anomaly</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((tx) => (
              <tr key={tx.eth_tx_hash} className="border-t border-slate-800">
                <td className="p-2">{tx.eth_tx_hash}</td>
                <td className="p-2">{tx.amount_eth}</td>
                <td className="p-2">{tx.risk_score}</td>
                <td className="p-2">{String(tx.anomaly_flag)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
