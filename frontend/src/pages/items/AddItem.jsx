import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../../app/layout/DashboardLayout";
import { ArrowLeft, Save } from "lucide-react";
import { createItem } from "@/services/items_service";
import toast from "react-hot-toast";

export default function AddItem() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    hsn_sac: "",
    uom: "PCS",
    rate: "",
    gst_percentage: "18",
    description: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      setLoading(true);
      await createItem({
        name: formData.name,
        hsn_sac: formData.hsn_sac,
        uom: formData.uom,
        rate: formData.rate,
        gst_percentage: formData.gst_percentage,
        description: formData.description,
      });
      toast.success("Item added successfully 🎉");
      navigate("/items");
    } catch (err) {
      toast.error(err.message || "Failed to add item");
    } finally {
      setLoading(false);
    }
  }

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        {/* <div className="flex items-center gap-4 mb-8"></div> */}

        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="bg-white rounded-2xl shadow-lg p-8"
        >
          <div className="mb-6 flex items-center justify-between gap-4">
            <h1 className="text-3xl font-bold text-gray-800">Add New Item</h1>
            <button
              type="button"
              onClick={() => navigate("/items")}
              className="flex items-center gap-2 bg-red-600 hover:bg-red-700 disabled:opacity-50 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 shadow-md hover:shadow-lg"
            >
              <ArrowLeft size={16} />
              Back
            </button>
          </div>

          <div className="border-b border-gray-200 mb-3"></div>

          {/* <p className="text-gray-500 mt-1">Create a new inventory item</p> */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Item Name Field */}
            <div>
              <label
                htmlFor="name"
                className="block text-sm font-semibold text-gray-700 mb-2"
              >
                Item Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="e.g., Steel Rod, Brick"
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
              />
            </div>

            {/* HSN/SAC Code Field */}
            <div>
              <label
                htmlFor="hsn_sac"
                className="block text-sm font-semibold text-gray-700 mb-2"
              >
                HSN/SAC Code
              </label>
              <input
                type="text"
                id="hsn_sac"
                name="hsn_sac"
                value={formData.hsn_sac}
                onChange={handleChange}
                placeholder="e.g., 7214"
                maxLength="8"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
              />
            </div>

            {/* UOM Field */}
            <div>
              <label
                htmlFor="uom"
                className="block text-sm font-semibold text-gray-700 mb-2"
              >
                Unit of Measure <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                id="uom"
                name="uom"
                value={formData.uom}
                onChange={handleChange}
                placeholder="e.g., PCS, KG, L, BOX"
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
              />
            </div>

            {/* Rate Field */}
            <div>
              <label
                htmlFor="rate"
                className="block text-sm font-semibold text-gray-700 mb-2"
              >
                Rate <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <span className="absolute left-3 top-2.5 text-gray-600">₹</span>
                <input
                  type="number"
                  id="rate"
                  name="rate"
                  value={formData.rate}
                  onChange={handleChange}
                  placeholder="0.00"
                  step="1"
                  min="0"
                  required
                  className="w-full pl-8 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                />
              </div>
            </div>

            {/* GST Percentage Field */}
            <div>
              <label
                htmlFor="gst_percentage"
                className="block text-sm font-semibold text-gray-700 mb-2"
              >
                GST % <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <input
                  type="number"
                  id="gst_percentage"
                  name="gst_percentage"
                  value={formData.gst_percentage}
                  onChange={handleChange}
                  placeholder="0.00"
                  step="0.01"
                  min="0"
                  max="100"
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                />
                <span className="absolute right-3 top-2.5 text-gray-600">
                  %
                </span>
              </div>
            </div>

            {/* Description Field */}
            <div className="md:col-span-2">
              <label
                htmlFor="description"
                className="block text-sm font-semibold text-gray-700 mb-2"
              >
                Description
              </label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="Enter item description (optional)"
                rows="4"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
              />
            </div>
          </div>

          {/* Form Actions */}
          <div className="flex gap-4 pt-6 border-t border-gray-200 mt-8">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 flex items-center justify-center gap-2 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 disabled:opacity-50 text-white font-semibold py-3 rounded-lg transition duration-200 shadow-md hover:shadow-lg"
            >
              <Save size={20} />
              {loading ? "Adding..." : "Add Item"}
            </button>
          </div>
        </form>
      </div>
    </DashboardLayout>
  );
}
