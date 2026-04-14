import { useState } from "react";
import { useProtocolStore } from "../store/useProtocolStore";

export default function SendTransactionPage() {
  const { currentAddress, riskScore, sendTransaction } = useProtocolStore();
  const [recipient, setRecipient] = useState("");
  const [amount, setAmount] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    await sendTransaction({
      sender: currentAddress,
      recipient,
      amount_eth: Number(amount),
      eth_tx_hash: `0xmock${Date.now().toString(16)}`,
    });
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Send Transaction</h2>
      <div className="rounded border border-slate-800 p-4">Predicted/Current Risk: {riskScore.toFixed(2)}</div>
      <form onSubmit={submit} className="space-y-2">
        <input value={recipient} onChange={(e) => setRecipient(e.target.value)} placeholder="Recipient address" className="w-full rounded bg-slate-900 p-2" />
        <input value={amount} onChange={(e) => setAmount(e.target.value)} placeholder="Amount ETH" className="w-full rounded bg-slate-900 p-2" />
        <button className="rounded bg-emerald-600 px-4 py-2">Submit</button>
      </form>
    </div>
  );
}
