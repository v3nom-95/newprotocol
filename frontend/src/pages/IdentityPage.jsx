import { useState } from "react";
import { useProtocolStore } from "../store/useProtocolStore";

export default function IdentityPage() {
  const [address, setAddress] = useState("");
  const { identity, createIdentity, setCurrentAddress } = useProtocolStore();

  const submit = async (e) => {
    e.preventDefault();
    await createIdentity(address);
    setCurrentAddress(address);
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Identity</h2>
      <form onSubmit={submit} className="flex gap-2">
        <input value={address} onChange={(e) => setAddress(e.target.value)} placeholder="0x..." className="w-full rounded bg-slate-900 p-2" />
        <button className="rounded bg-indigo-600 px-4 py-2">Create</button>
      </form>
      {identity && (
        <div className="rounded border border-slate-800 p-4 text-sm">
          <div>DID: {identity.did}</div>
          <div>DID Hash: {identity.did_hash}</div>
          <div>PQ Public Key: {identity.pq_public_key}</div>
        </div>
      )}
    </div>
  );
}
