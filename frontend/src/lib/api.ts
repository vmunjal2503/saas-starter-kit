/**
 * API client — centralized HTTP client for backend communication.
 */

import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 — refresh token or redirect to login
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Try refreshing the token
      const refreshToken = localStorage.getItem("refresh_token");
      if (refreshToken) {
        try {
          const { data } = await axios.post(`${API_BASE}/api/auth/refresh`, null, {
            params: { refresh_token: refreshToken },
          });
          localStorage.setItem("access_token", data.access_token);
          localStorage.setItem("refresh_token", data.refresh_token);
          error.config.headers.Authorization = `Bearer ${data.access_token}`;
          return api.request(error.config);
        } catch {
          localStorage.clear();
          window.location.href = "/login";
        }
      }
    }
    return Promise.reject(error);
  }
);

// ──────────────── Auth API ────────────────
export const authAPI = {
  register: (data: { email: string; password: string; full_name: string }) =>
    api.post("/api/auth/register", data),
  login: (data: { email: string; password: string }) =>
    api.post("/api/auth/login", data),
  forgotPassword: (email: string) =>
    api.post("/api/auth/forgot-password", { email }),
};

// ──────────────── User API ────────────────
export const userAPI = {
  getProfile: () => api.get("/api/users/me"),
  updateProfile: (data: { full_name?: string }) => api.patch("/api/users/me", data),
};

// ──────────────── Organization API ────────────────
export const orgAPI = {
  list: () => api.get("/api/organizations"),
  create: (data: { name: string }) => api.post("/api/organizations", data),
  getMembers: (orgId: string) => api.get(`/api/organizations/${orgId}/members`),
  inviteMember: (orgId: string, data: { email: string; role: string }) =>
    api.post(`/api/organizations/${orgId}/invite`, data),
};

// ──────────────── Billing API ────────────────
export const billingAPI = {
  getSubscription: (orgId: string) => api.get(`/api/billing/subscription/${orgId}`),
  createCheckout: (data: { plan: string; org_id: string }) =>
    api.post("/api/billing/checkout", data),
  openPortal: (orgId: string) => api.post(`/api/billing/portal/${orgId}`),
};

export default api;
