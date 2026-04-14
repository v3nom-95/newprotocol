import { Link, Route, Routes } from "react-router-dom";
import { Navigate } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import IdentityPage from "./pages/IdentityPage";
import SendTransactionPage from "./pages/SendTransactionPage";
import ExplorerPage from "./pages/ExplorerPage";
import AdminPage from "./pages/AdminPage";
import LoginPage from "./pages/LoginPage";
import { useProtocolStore } from "./store/useProtocolStore";

const nav = [
  ["Dashboard", "/"],
  ["Identity", "/identity"],
  ["Send Transaction", "/send"],
  ["Explorer", "/explorer"],
  ["Admin", "/admin"],
];

export default function App() {
  const { auth, logout } = useProtocolStore();
  const isAuthenticated = Boolean(auth?.accessToken);

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 px-6 py-4">
        <h1 className="text-2xl font-semibold">Q-AI Chain</h1>
        <div className="mt-2 flex items-center justify-between text-xs text-slate-400">
          <span>{auth.email} ({auth.role})</span>
          <button onClick={logout} className="rounded bg-slate-800 px-2 py-1 text-slate-200 hover:bg-slate-700">Logout</button>
        </div>
        <nav className="mt-3 flex gap-4 text-sm">
          {nav.map(([label, to]) => (
            <Link key={to} to={to} className="text-slate-300 hover:text-white">
              {label}
            </Link>
          ))}
        </nav>
      </header>
      <main className="p-6">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/identity" element={<IdentityPage />} />
          <Route path="/send" element={<SendTransactionPage />} />
          <Route path="/explorer" element={<ExplorerPage />} />
          <Route path="/admin" element={<AdminPage />} />
        </Routes>
      </main>
    </div>
  );
}
