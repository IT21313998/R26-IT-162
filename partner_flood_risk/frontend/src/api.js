import axios from 'axios';

const BASE_URL = 'http://localhost:5000';

const api = axios.create({ baseURL: BASE_URL });

export const getOptions = () => api.get('/api/options');

export const predict = (payload) => api.post('/api/predict', payload);

export const healthCheck = () => api.get('/api/health');
