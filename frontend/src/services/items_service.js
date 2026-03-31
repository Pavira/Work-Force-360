import api from "@/config/axios";

// Create item
export const createItem = async (payload) => {
  const res = await api.post("/items", payload);
  console.log("Create Item Response:", res.data);
  return res.data;
};

// Update item
export const updateItem = async (itemId, payload) => {
  const res = await api.put(`/items/${itemId}`, payload);
  console.log("Update Item Response:", res.data);
  return res.data;
};

// Delete item (soft delete)
export const deleteItem = async (itemId) => {
  const res = await api.delete(`/items/${itemId}`);
  return res.data;
};

// Get all items
export const getAllItems = async () => {
  const res = await api.get("/items");
  return res.data;
};

// Get item by ID
export const getItemById = async (itemId) => {
  const res = await api.get(`/items/${itemId}`);
  return res.data;
};
