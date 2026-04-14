import { create } from "zustand";
import { api } from "../services/api";

export const useProtocolStore = create((set, get) => ({
  currentAddress: "",
  riskScore: 0,
  transactions: [],
  identity: null,
  setCurrentAddress: (address) => set({ currentAddress: address }),
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
  sendTransaction: async (payload) => {
    await api.post("/transactions", payload);
    if (payload.sender) {
      await get().fetchTransactions(payload.sender);
      await get().fetchRisk(payload.sender);
    }
  },
}));
