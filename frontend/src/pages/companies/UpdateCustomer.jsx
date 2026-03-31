import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import DashboardLayout from "../../app/layout/DashboardLayout";
import { ArrowLeft, Save, Trash2 } from "lucide-react";
import {
  updateCustomer,
  deleteCustomer,
  getCustomerById,
} from "@/services/customer_service";
import toast from "react-hot-toast";

export default function UpdateCustomer() {
  const { customerId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    address: "",
    gstin: "",
    panNumber: "",
  });

  useEffect(() => {
    if (customerId) {
      fetchCustomer();
    }
  }, [customerId]);

  const fetchCustomer = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getCustomerById(customerId);
      const customer = response.customer;

      setFormData({
        name: customer.name || "",
        email: customer.email || "",
        phone: customer.phone || "",
        address: customer.address || "",
        gstin: customer.gstin || "",
        panNumber: customer.panNumber || "",
      });
    } catch (err) {
      setError("Failed to load customer details");
      console.error("Error fetching customer:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      setError(null);
      await updateCustomer(customerId, {
        name: formData.name,
        email: formData.email,
        phone: formData.phone,
        address: formData.address,
        gstin: formData.gstin,
        panNumber: formData.panNumber,
      });
      toast.success(`Customer ${formData.name} updated successfully 🎉`);
      //   setTimeout(() => {
      navigate("/customers");
      //   }, 1500);
    } catch (err) {
      setError("Failed to update customer");
      toast.error("Failed to update customer");
      console.error("Error updating customer:", err);
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (
      window.confirm(
        "Are you sure you want to delete this customer? This action cannot be undone.",
      )
    ) {
      try {
        setSaving(true);
        await deleteCustomer(customerId);
        toast.success("Customer deleted successfully");
        navigate("/customers");
      } catch (err) {
        setError("Failed to delete customer");
        toast.error("Failed to delete customer");
        console.error("Error deleting customer:", err);
        setSaving(false);
      }
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

  return (
    <DashboardLayout>
      <div className="w-full">
        <div className="bg-white rounded-2xl shadow-lg p-8">
          {error && (
            <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-8">
            <div className="mb-6 flex items-center justify-between gap-4">
              <h1 className="text-3xl font-bold text-gray-800">
                Edit customer details
              </h1>
              <button
                type="button"
                onClick={() => navigate("/customers")}
                className="flex items-center gap-2 bg-red-600 hover:bg-red-700 disabled:opacity-50 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 shadow-md hover:shadow-lg"
              >
                <ArrowLeft size={16} />
                Back
              </button>
            </div>

            <div className="border-b border-gray-200 mb-3"></div>

            {/* Basic Information Section */}
            <div>
              <h2 className="text-xl font-bold text-gray-800 mb-4 pb-2 border-b-2 border-purple-200">
                Basic Information
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Customer Name */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Customer Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="Enter customer name"
                  />
                </div>

                {/* Email */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Email <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="Enter email address"
                  />
                </div>

                {/* Phone Number */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="Enter phone number"
                  />
                </div>

                {/* GSTIN */}
                {/* <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  GSTIN
                </label>
                <input
                  type="text"
                  name="gstin"
                  value={formData.gstin}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="Enter GSTIN (15 digits)"
                  maxLength="15"
                />
              </div> */}

                {/* Address */}
                <div className="md:col-span-2">
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Address
                  </label>
                  <textarea
                    name="address"
                    value={formData.address}
                    onChange={handleChange}
                    rows="3"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="Enter customer address"
                  />
                </div>
              </div>
            </div>
            {/* Tax Information Section */}
            <div>
              <h2 className="text-xl font-bold text-gray-800 mb-4 pb-2 border-b-2 border-purple-200">
                Tax Information
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* GSTIN/UIN Field */}
                <div>
                  <label
                    htmlFor="gstinUin"
                    className="block text-sm font-semibold text-gray-700 mb-2"
                  >
                    GSTIN/UIN <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    name="gstin"
                    value={formData.gstin}
                    onChange={handleChange}
                    placeholder="Enter GSTIN/UIN (15 digits)"
                    required
                    maxLength="15"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Goods and Services Tax Identification Number
                  </p>
                </div>

                {/* PAN Number Field */}
                <div>
                  <label
                    htmlFor="panNumber"
                    className="block text-sm font-semibold text-gray-700 mb-2"
                  >
                    PAN Number
                    {/* <span className="text-red-500">*</span> */}
                  </label>
                  <input
                    type="text"
                    id="panNumber"
                    name="panNumber"
                    value={formData.panNumber}
                    onChange={handleChange}
                    placeholder="Enter PAN number (10 characters)"
                    maxLength="10"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Permanent Account Number for income tax
                  </p>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4 mt-8 pt-6 border-t border-gray-200">
              <button
                type="submit"
                disabled={saving}
                className="flex-1 flex items-center justify-center gap-2 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 disabled:opacity-50 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 shadow-md hover:shadow-lg"
              >
                <Save size={20} />
                {saving ? "Saving..." : "Save Changes"}
              </button>
              <button
                type="button"
                onClick={handleDelete}
                disabled={saving}
                className="flex-1 flex items-center gap-2 bg-red-600 hover:bg-red-700 disabled:opacity-50 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 shadow-md hover:shadow-lg justify-center"
              >
                <Trash2 size={20} />
                Delete
              </button>
            </div>
          </form>

          {/* Loading Overlay */}
          {saving && (
            <div className="fixed inset-0 bg-black bg-opacity-30 backdrop-blur-sm flex justify-center items-center z-50">
              <div className="flex flex-col items-center gap-4">
                <div className="animate-spin rounded-full h-16 w-16 border-4 border-purple-200 border-t-purple-600"></div>
                <p className="text-gray-700 font-semibold text-lg">
                  Updating customer...
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
