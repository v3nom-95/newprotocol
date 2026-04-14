import { Link, Route, Routes } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import IdentityPage from "./pages/IdentityPage";
import SendTransactionPage from "./pages/SendTransactionPage";
import ExplorerPage from "./pages/ExplorerPage";
import AdminPage from "./pages/AdminPage";

const nav = [
  ["Dashboard", "/"],
  ["Identity", "/identity"],
  ["Send Transaction", "/send"],
  ["Explorer", "/explorer"],
  ["Admin", "/admin"],
];

export default function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 px-6 py-4">
        <h1 className="text-2xl font-semibold">Q-AI Chain</h1>
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
