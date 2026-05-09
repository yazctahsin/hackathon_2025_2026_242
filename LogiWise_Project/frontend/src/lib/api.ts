import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', 
});

export const getAiSummary = async () => {
  const response = await api.get('/ai-summary');
  return response.data;
};

export const getOrders = async () => {
  const response = await api.get('/orders');
  return response.data;
};

export const runGhostSupport = async () => {
  const response = await api.get('/ghost-support/auto-action');
  return response.data;
};