import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API endpoints
export const apiService = {
  // Health check
  healthCheck: () => api.get('/health'),

  // Historical data
  getHistoricalData: (params = {}) => api.get('/data/historical', { params }),
  
  // Data summary
  getDataSummary: () => api.get('/data/summary'),

  // Events
  getEvents: (params = {}) => api.get('/events', { params }),
  getEventTypes: () => api.get('/events/types'),

  // Analysis
  getEventCorrelation: (params = {}) => api.get('/analysis/correlation', { params }),
  getVolatilityAnalysis: (params = {}) => api.get('/analysis/volatility', { params }),
  getChangePoints: () => api.get('/analysis/changepoints'),
  getPerformanceMetrics: () => api.get('/analysis/metrics'),
};

export default api;
