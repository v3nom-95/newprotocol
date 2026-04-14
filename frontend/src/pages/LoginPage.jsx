import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useProtocolStore } from "../store/useProtocolStore";

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useProtocolStore();
  const [email, setEmail] = useState("admin@qai.local");
  const [password, setPassword] = useState("Admin@123");
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      navigate("/");
    } catch (err) {
      setError(err?.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div className="mx-auto mt-10 max-w-md rounded border border-slate-800 p-6">
      <h2 className="mb-4 text-xl font-semibold">Protocol Login</h2>
      <form onSubmit={submit} className="space-y-3">
        <input className="w-full rounded bg-slate-900 p-2" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input
          type="password"
          className="w-full rounded bg-slate-900 p-2"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && <div className="text-sm text-red-400">{error}</div>}
        <button className="rounded bg-indigo-600 px-4 py-2">Login</button>
      </form>
    </div>
  );
}
