import React, { createContext, useContext, useEffect, useState } from 'react';
import axios from 'axios';

// Create a context to store authentication state and helper functions.

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('authToken'));
  const [user, setUser] = useState(null);

  // Configure axios with a default base URL. Adjust the URL according to
  // where the backend is hosted. During development you might run
  // frontend at port 3000 and backend at 8000, so update this string
  // accordingly.
  const api = axios.create({
    baseURL: 'http://localhost:8000/api/',
  });

  // Attach token to every request if present
  api.interceptors.request.use((config) => {
    if (token) {
      config.headers['Authorization'] = `Token ${token}`;
    }
    return config;
  });

  // Simple helper to decode username from token if needed. Our backend
  // does not encode user info in the token, so we fetch user on login.

  const login = async (username, password) => {
    const response = await api.post('auth/login/', { username, password });
    setToken(response.data.token);
    localStorage.setItem('authToken', response.data.token);
    // Optionally fetch user profile here
  };

  const register = async (username, email, password) => {
    const response = await api.post('auth/register/', {
      username,
      email,
      password,
    });
    setToken(response.data.token);
    localStorage.setItem('authToken', response.data.token);
  };

  const logout = async () => {
    try {
      await api.post('auth/logout/');
    } catch (e) {
      // ignore
    }
    setToken(null);
    setUser(null);
    localStorage.removeItem('authToken');
  };

  // Provide the API instance so that components can perform requests
  const value = {
    token,
    user,
    api,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
