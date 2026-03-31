import api from "@/config/axios";

// Get all approved companies
export const getAllApprovedCompanies = async () => {
  const res = await api.get("/admin_panel_company/all_approved_companies");
  return res.data;
};

// Get all approved companies
export const getAllUnApprovedCompanies = async () => {
  const res = await api.get("/admin_panel_company/all_unapproved_companies");
  return res.data;
};

// Get all draft companies
export const getAllDraftCompanies = async () => {
  const res = await api.get("/admin_panel_company/all_draft_companies");
  return res.data;
};

// Get Company by ID from admin panel routes
export const getCompanyById = async (companyId) => {
  const res = await api.get(`/admin_panel_company/${companyId}`);
  return res.data;
};

// Approve Company
export const approveCompany = async (companyId) => {
  const res = await api.patch(
    `/admin_panel_company/approve_company_profile/${companyId}`,
  );
  return res.data;
};

// Unapprove Company
export const unapproveCompany = async (companyId) => {
  // TODO: Add backend endpoint
  const res = await api.patch(`/admin_panel_company/unapprove/${companyId}`);
  return res.data;
};

// Reject Company
export const rejectCompany = async (companyId) => {
  // TODO: Add backend endpoint
  const res = await api.patch(`/admin_panel_company/reject/${companyId}`);
  return res.data;
};
