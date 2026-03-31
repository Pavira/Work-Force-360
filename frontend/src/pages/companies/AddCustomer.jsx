import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../../app/layout/DashboardLayout";
import { ArrowLeft } from "lucide-react";
import { createCustomer } from "../../services/customer_service";
import toast from "react-hot-toast";

export default function AddCustomer() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    customerName: "",
    email: "",
    phoneNumber: "",
    address: "",
    gstinUin: "",
    panNumber: "",
    // contactPersonName: "",
    // contactPhoneNumber: "",
    // contactPersonEmail: "",
  });

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
      const payload = {
        name: formData.customerName,
        email: formData.email,
        phone: formData.phoneNumber,
        address: formData.address,
        gstin: formData.gstinUin,
        panNumber: formData.panNumber || "",
      };
      await createCustomer(payload);
      toast.success("Customer added successfully 🎉");
      navigate("/customers");
    } catch (error) {
      console.error("Error creating customer:", error);
    }
  };

  return (
    <DashboardLayout>
      <div className="w-full">
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Center the Heading and underline */}
            <div className="mb-6 flex items-center justify-between gap-4">
              <h1 className="text-3xl font-bold text-gray-800">
                Add New Customer
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
                {/* Customer Name Field */}
                <div>
                  <label
                    htmlFor="customerName"
                    className="block text-sm font-semibold text-gray-700 mb-2"
                  >
                    Customer Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    id="customerName"
                    name="customerName"
                    value={formData.customerName}
                    onChange={handleChange}
                    placeholder="Enter customer name"
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  />
                </div>

                {/* Email Field */}
                <div>
                  <label
                    htmlFor="email"
                    className="block text-sm font-semibold text-gray-700 mb-2"
                  >
                    Email Address <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Enter email address"
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  />
                </div>

                {/* Phone Number Field */}
                <div>
                  <label
                    htmlFor="phoneNumber"
                    className="block text-sm font-semibold text-gray-700 mb-2"
                  >
                    Phone Number <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="tel"
                    id="phoneNumber"
                    name="phoneNumber"
                    value={formData.phoneNumber}
                    onChange={handleChange}
                    placeholder="Enter phone number eg. 9234567890, 9234567890"
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  />
                </div>

                {/* Address Field - Full width */}
                <div className="md:col-span-2">
                  <label
                    htmlFor="address"
                    className="block text-sm font-semibold text-gray-700 mb-2"
                  >
                    Address <span className="text-red-500">*</span>
                  </label>
                  <textarea
                    id="address"
                    name="address"
                    value={formData.address}
                    onChange={handleChange}
                    placeholder="Enter customer address (street, city, state, postal code)"
                    required
                    rows="3"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition resize-none"
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
                    id="gstinUin"
                    name="gstinUin"
                    value={formData.gstinUin}
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

            {/* Contact Person Information Section */}
            {/* <div>
              <h2 className="text-xl font-bold text-gray-800 mb-4 pb-2 border-b-2 border-purple-200">
                Contact Person Information
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                Contact Person Name Field
                <div>
                  <label
                    htmlFor="contactPersonName"
                    className="block text-sm font-semibold text-gray-700 mb-2"
                  >
                    Contact Person Name
                    <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    id="contactPersonName"
                    name="contactPersonName"
                    value={formData.contactPersonName}
                    onChange={handleChange}
                    placeholder="Enter contact person name"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  />
                </div>

                Contact Phone Number Field
                <div>
                  <label
                    htmlFor="contactPhoneNumber"
                    className="block text-sm font-semibold text-gray-700 mb-2"
                  >
                    Contact Phone Number
                    <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="tel"
                    id="contactPhoneNumber"
                    name="contactPhoneNumber"
                    value={formData.contactPhoneNumber}
                    onChange={handleChange}
                    placeholder="Enter contact person phone number"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  />
                </div>

                Contact Person Email Field
                <div className="md:col-span-2">
                  <label
                    htmlFor="contactPersonEmail"
                    className="block text-sm font-semibold text-gray-700 mb-2"
                  >
                    Contact Person Email
                    <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="email"
                    id="contactPersonEmail"
                    name="contactPersonEmail"
                    value={formData.contactPersonEmail}
                    onChange={handleChange}
                    placeholder="Enter contact person email address"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  />
                </div>
              </div>
            </div> */}

            {/* Form Actions */}
            <div className="flex gap-4 pt-6 border-t border-gray-200">
              <button
                type="submit"
                className="flex-1 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white font-semibold py-3 rounded-lg transition duration-200 shadow-md hover:shadow-lg"
              >
                Add Customer
              </button>
            </div>
          </form>
        </div>
      </div>
    </DashboardLayout>
  );
}
