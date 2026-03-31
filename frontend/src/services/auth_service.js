import api from "@/config/axios";

export const loginWithPin = async (pin) => {
  try {
    const response = await api.post("/auth/verify-pin", { pin });
    return response.data;
  } catch (error) {
    if (error.response) {
      // Backend error (401, 400, 500)
      throw new Error(error.response.data.detail);
    } else {
      // Network / timeout error
      throw new Error("Server not reachable");
    }
  }
};
