import { useProtocolStore } from "../store/useProtocolStore";

export default function AdminPage() {
  const { transactions } = useProtocolStore();
  const anomalies = transactions.filter((tx) => tx.anomaly_flag).length;
  const total = transactions.length;
  const avgRisk = total
    ? transactions.reduce((acc, tx) => acc + Number(tx.risk_score || 0), 0) / total
    : 0;

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Admin Panel</h2>
      <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
        <div className="rounded border border-slate-800 p-4">Total TX: {total}</div>
        <div className="rounded border border-slate-800 p-4">Anomalies: {anomalies}</div>
        <div className="rounded border border-slate-800 p-4">Average Risk: {avgRisk.toFixed(2)}</div>
      </div>
    </div>
  );
}
