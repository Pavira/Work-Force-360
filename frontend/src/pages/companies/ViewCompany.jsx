import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import DashboardLayout from "../../app/layout/DashboardLayout";
import { Eye, CheckCircle, XCircle, AlertTriangle } from "lucide-react";
import {
  getCompanyById,
  approveCompany,
  unapproveCompany,
  rejectCompany,
} from "@/services/company_service";
import PageHeader from "@/components/ui/PageHeader";

export default function ViewCompany() {
  const navigate = useNavigate();
  const { companyId } = useParams();
  const [company, setCompany] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCompanyDetails();
  }, [companyId]);

  const fetchCompanyDetails = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getCompanyById(companyId);
      if (response && response.data) {
        setCompany(response.data);
      } else {
        throw new Error("Failed to fetch company details");
      }
    } catch (err) {
      setError("Failed to load company details");
      console.error("Error fetching company:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async () => {
    try {
      await approveCompany(companyId);
      // Refresh company details
      fetchCompanyDetails();
    } catch (err) {
      console.error("Error approving company:", err);
      setError("Failed to approve company");
    }
  };

  const handleUnapprove = async () => {
    try {
      await unapproveCompany(companyId);
      // Refresh company details
      fetchCompanyDetails();
    } catch (err) {
      console.error("Error unapproving company:", err);
      setError("Failed to unapprove company");
    }
  };

  const handleReject = async () => {
    try {
      await rejectCompany(companyId);
      // Refresh company details
      fetchCompanyDetails();
    } catch (err) {
      console.error("Error rejecting company:", err);
      setError("Failed to reject company");
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          {error}
        </div>
      </DashboardLayout>
    );
  }

  if (!company) {
    return (
      <DashboardLayout>
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">Company not found</p>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="bg-white rounded-2xl shadow-lg p-4 md:p-6">
        <PageHeader
          title="Company Details"
          subtitle="View company information"
        />

        {/* Basic Details */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-4">Basic Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Company Name
              </label>
              <p className="mt-1 text-sm text-gray-900">
                {company.company_name || "-"}
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Industry
              </label>
              <p className="mt-1 text-sm text-gray-900">
                {company.industry_name || "-"}
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                GST Number
              </label>
              <p className="mt-1 text-sm text-gray-900">
                {company.gst_number || "-"}
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Status
              </label>
              <p className="mt-1 text-sm text-gray-900">
                {company.status || "-"}
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Auth Phone
              </label>
              <p className="mt-1 text-sm text-gray-900">
                {company.auth_phone || "-"}
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Contact Person Name
              </label>
              <p className="mt-1 text-sm text-gray-900">
                {company.contact_person_name || "-"}
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Contact Phone
              </label>
              <p className="mt-1 text-sm text-gray-900">
                {company.contact_country_code && company.contact_phone
                  ? `${company.contact_country_code} ${company.contact_phone}`
                  : "-"}
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Contact Email
              </label>
              <p className="mt-1 text-sm text-gray-900">
                {company.contact_email || "-"}
              </p>
            </div>
            {company.logo_url && (
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Logo
                </label>
                <img
                  src={company.logo_url}
                  alt="Company Logo"
                  className="mt-1 w-16 h-16 object-cover rounded"
                />
              </div>
            )}
          </div>
        </div>

        {/* Address Details */}
        {company.addresses && company.addresses.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-4">Address Details</h3>
            {company.addresses.map((address, index) => (
              <div key={address.id} className="border rounded-lg p-4 mb-4">
                <h4 className="font-medium mb-2">Address {index + 1}</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Address
                    </label>
                    <p className="mt-1 text-sm text-gray-900">
                      {address.address || "-"}
                    </p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Unit Name
                    </label>
                    <p className="mt-1 text-sm text-gray-900">
                      {address.unit_name || "-"}
                    </p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      City
                    </label>
                    <p className="mt-1 text-sm text-gray-900">
                      {address.city || "-"}
                    </p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      State
                    </label>
                    <p className="mt-1 text-sm text-gray-900">
                      {address.state || "-"}
                    </p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Pincode
                    </label>
                    <p className="mt-1 text-sm text-gray-900">
                      {address.pincode || "-"}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Bank Details */}
        {company.bank_details && company.bank_details.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-4">Bank Details</h3>
            {company.bank_details.map((bank, index) => (
              <div key={bank.id} className="border rounded-lg p-4 mb-4">
                <h4 className="font-medium mb-2">Bank Account {index + 1}</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Bank Name
                    </label>
                    <p className="mt-1 text-sm text-gray-900">
                      {bank.bank_name || "-"}
                    </p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Account Holder Name
                    </label>
                    <p className="mt-1 text-sm text-gray-900">
                      {bank.account_holder_name || "-"}
                    </p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Account Number
                    </label>
                    <p className="mt-1 text-sm text-gray-900">
                      {bank.account_number || "-"}
                    </p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      IFSC Code
                    </label>
                    <p className="mt-1 text-sm text-gray-900">
                      {bank.ifsc_code || "-"}
                    </p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      UPI ID
                    </label>
                    <p className="mt-1 text-sm text-gray-900">
                      {bank.upi_id || "-"}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Documents */}
        {company.documents && company.documents.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-4">Documents</h3>
            {company.documents.map((doc, index) => (
              <div key={doc.id} className="border rounded-lg p-4 mb-4">
                <h4 className="font-medium mb-2">Document {index + 1}</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Document Type
                    </label>
                    <p className="mt-1 text-sm text-gray-900">
                      {doc.document_type || "-"}
                    </p>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Document URL
                    </label>
                    <a
                      href={doc.document_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="mt-1 text-sm text-blue-600 hover:text-blue-800"
                    >
                      View Document
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
        {/* Action Buttons */}
        <div className="mb-6 flex flex-wrap gap-3">
          <button
            onClick={handleApprove}
            className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition duration-200"
          >
            <CheckCircle size={18} />
            Approve
          </button>
          <button
            onClick={handleUnapprove}
            className="flex items-center gap-2 bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg transition duration-200"
          >
            <AlertTriangle size={18} />
            Unapprove
          </button>
          <button
            onClick={handleReject}
            className="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition duration-200"
          >
            <XCircle size={18} />
            Reject
          </button>
        </div>
      </div>
    </DashboardLayout>
  );
}
