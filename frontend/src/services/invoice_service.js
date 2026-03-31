import api from "@/config/axios";

// Get preview invoice number
export const getPreviewInvoiceNumber = async () => {
  const res = await api.get("/invoices/preview-invoice-number");
  return res.data;
};

// Create invoice
export const createInvoice = async (payload) => {
  const res = await api.post("/invoices", payload);
  console.log("Create Invoice Response:", res.data);
  return res.data;
};

// Get all invoices
export const getAllInvoices = async () => {
  const res = await api.get("/invoices");
  return res.data;
};

// Get invoice by ID
export const getInvoiceById = async (invoiceId) => {
  const res = await api.get(`/invoices/${invoiceId}`);
  return res.data;
};

// Update invoice
export const updateInvoice = async (invoiceId, payload) => {
  const res = await api.put(`/invoices/${invoiceId}`, payload);
  console.log("Update Invoice Response:", res.data);
  return res.data;
};

// Delete invoice
export const deleteInvoice = async (invoiceId) => {
  const res = await api.delete(`/invoices/${invoiceId}`);
  return res.data;
};

export const getInvoicePDF = async (invoiceId) => {
  const res = await api.get(`/invoices/${invoiceId}/pdf`, {
    responseType: "blob",
  });
  return res.data;
};
