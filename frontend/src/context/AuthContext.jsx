import React, { createContext, useState, useEffect } from "react";
import axios from "axios";

const AuthContext = createContext();

const BASE_API_URL = import.meta.env.VITE_BASE_API_URL;

export const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem("authTokens") ? JSON.parse(localStorage.getItem("authTokens")) : null
  );
  const [user, setUser] = useState(() =>
    authTokens ? JSON.parse(atob(authTokens.access.split(".")[1])) : null
  );

  const register = async (usn, name, email, password) => {
    await axios.post(`${BASE_API_URL}/api/students/register/`, {
      usn,
      name,
      email,
      password,
      subjects: [],
      enrolled_subjects: [],
    });
    // alert("Registration successful! Please log in.");
  };

  const login = async (username, password) => {
    console.log(BASE_API_URL)
    const response = await axios.post(`${BASE_API_URL}/api/students/login/`, {
      username,
      password,
    });
    setAuthTokens(response.data);
    setUser(JSON.parse(atob(response.data.access.split(".")[1])));
    localStorage.setItem("authTokens", JSON.stringify(response.data));
  };

  const logout = async () => {
    await axios.post(`${BASE_API_URL}/api/students/logout/`, {
      refresh: authTokens.refresh,
    });
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem("authTokens");
  };

  const refreshToken = async () => {
    const response = await axios.post(`${BASE_API_URL}/api/students/token/refresh/`, {
      refresh: authTokens.refresh,
    });
    setAuthTokens((prevTokens) => ({ ...prevTokens, access: response.data.access }));
    localStorage.setItem("authTokens", JSON.stringify({ ...authTokens, access: response.data.access }));
  };

  useEffect(() => {
    if (authTokens) {
      const interval = setInterval(() => {
        refreshToken();
      }, 10 * 60 * 1000); // Refresh token every 4 minutes
      return () => clearInterval(interval);
    }
  }, [authTokens]);

  return (
    <AuthContext.Provider value={{ user, authTokens, register, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
