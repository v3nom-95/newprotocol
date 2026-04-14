import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 10,
  duration: "30s",
};

const BASE = __ENV.BASE_URL || "http://localhost:8000/api/v1";
const TOKEN = __ENV.ACCESS_TOKEN || "";

export default function () {
  const headers = TOKEN ? { Authorization: `Bearer ${TOKEN}` } : {};
  const res = http.get(`${BASE}/health`, { headers });
  check(res, { "status 200": (r) => r.status === 200 });
  sleep(1);
}
