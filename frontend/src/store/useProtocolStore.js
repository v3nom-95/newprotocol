import { create } from "zustand";
import { api, setAccessToken } from "../services/api";

export const useProtocolStore = create((set, get) => ({
  auth: {
    email: "",
    role: "",
    accessToken: "",
    refreshToken: "",
  },
  currentAddress: "",
  riskScore: 0,
  transactions: [],
  predictedRisk: null,
  identity: null,
  setCurrentAddress: (address) => set({ currentAddress: address }),
  login: async (email, password) => {
    const { data } = await api.post("/auth/login", { email, password });
    set({
      auth: {
        email,
        role: data.role,
        accessToken: data.access_token,
        refreshToken: data.refresh_token,
      },
    });
    setAccessToken(data.access_token);
  },
  logout: () => {
    set({
      auth: { email: "", role: "", accessToken: "", refreshToken: "" },
      currentAddress: "",
      transactions: [],
      identity: null,
      riskScore: 0,
    });
    setAccessToken("");
  },
  fetchIdentity: async (address) => {
    const { data } = await api.get(`/identity/${address}`);
    set({ identity: data });
  },
  createIdentity: async (address) => {
    const { data } = await api.post("/identity", { eth_address: address });
    set({ identity: data, currentAddress: address });
  },
  fetchRisk: async (address) => {
    const { data } = await api.get(`/risk/${address}`);
    set({ riskScore: data.score });
  },
  fetchTransactions: async (address) => {
    const { data } = await api.get(`/transactions/${address}`);
    set({ transactions: data });
  },
  predictRisk: async (sender, amountEth) => {
    const { data } = await api.post("/transactions/predict-risk", {
      sender,
      amount_eth: Number(amountEth),
    });
    set({ predictedRisk: data });
  },
  sendTransaction: async (payload) => {
    await api.post("/transactions", payload);
    if (payload.sender) {
      await get().fetchTransactions(payload.sender);
      await get().fetchRisk(payload.sender);
    }
  },
}));
