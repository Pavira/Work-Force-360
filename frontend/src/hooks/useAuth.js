import { useState } from "react";

export function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const login = async (pin) => {
    setLoading(true);
    setError(null);
    try {
      // TODO: Call auth service
      console.log("Logging in with PIN:", pin);
      setUser({ id: 1, name: "Admin", email: "admin@spm.com" });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("authToken");
  };

  return { user, loading, error, login, logout };
}
