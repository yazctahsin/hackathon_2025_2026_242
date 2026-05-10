import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const notifyCustomer = async (
  customer_name: string,
  message: string,
  channel: "sms" | "email"
) => {
  const response = await api.post("/notify/customer", {
    customer_name,
    message,
    channel,
  });

  return response.data;
};

export const getAiSummary = async () => {
  const response = await api.get("/ai-summary");
  return response.data;
};

export const getOrders = async () => {
  const response = await api.get("/orders");
  return response.data;
};

export const runGhostSupport = async () => {
  const response = await api.get("/ghost-support/auto-action");
  return response.data;
};