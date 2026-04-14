import axios from "axios";

const API_URL = process.env.QAI_API_URL || "http://localhost:8000/api/v1";

export async function getRiskScore(address) {
  const { data } = await axios.get(`${API_URL}/risk/${address}`);
  return data;
}
