/**
 * Authentication hook — login, register, logout, current user.
 */

import { useState, useEffect } from "react";
import { authAPI, userAPI } from "../lib/api";

interface User {
  id: string;
  email: string;
  full_name: string;
  is_verified: boolean;
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      userAPI
        .getProfile()
        .then((res) => setUser(res.data))
        .catch(() => localStorage.clear())
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    const { data } = await authAPI.login({ email, password });
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    const profile = await userAPI.getProfile();
    setUser(profile.data);
  };

  const register = async (email: string, password: string, full_name: string) => {
    const { data } = await authAPI.register({ email, password, full_name });
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    const profile = await userAPI.getProfile();
    setUser(profile.data);
  };

  const logout = () => {
    localStorage.clear();
    setUser(null);
    window.location.href = "/login";
  };

  return { user, loading, login, register, logout, isAuthenticated: !!user };
}
