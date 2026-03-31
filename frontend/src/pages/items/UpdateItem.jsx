import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import DashboardLayout from "../../app/layout/DashboardLayout";
import { ArrowLeft, Save, Trash2 } from "lucide-react";
import { updateItem, deleteItem, getItemById } from "@/services/items_service";
import toast from "react-hot-toast";

export default function UpdateItem() {
  const { itemId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    hsn_sac: "",
    uom: "",
    rate: "",
    gst_percentage: "",
  });

  useEffect(() => {
    if (itemId) {
      fetchItem();
    }
  }, [itemId]);

  const fetchItem = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getItemById(itemId);
      const item = response.item;

      setFormData({
        name: item.name || "",
        description: item.description || "",
        hsn_sac: item.hsn_sac || "",
        uom: item.uom || "",
        rate: item.rate || "",
        gst_percentage: item.gst_percentage || "",
      });
    } catch (err) {
      setError("Failed to load item details");
      console.error("Error fetching item:", err);
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
      await updateItem(itemId, {
        name: formData.name,
        description: formData.description,
        hsn_sac: formData.hsn_sac,
        uom: formData.uom,
        rate: formData.rate,
        gst_percentage: formData.gst_percentage,
      });
      toast.success("Item updated successfully 🎉");
      // setTimeout(() => {
      navigate("/items");
      // }, 1000);
    } catch (err) {
      setError("Failed to update item");
      toast.error("Failed to update item");
      console.error("Error updating item:", err);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (
      window.confirm(
        "Are you sure you want to delete this item? This action cannot be undone.",
      )
    ) {
      try {
        setSaving(true);
        await deleteItem(itemId);
        toast.success("Item deleted successfully");
        navigate("/items");
      } catch (err) {
        setError("Failed to delete item");
        toast.error("Failed to delete item");
        console.error("Error deleting item:", err);
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
      <div className="max-w-4xl mx-auto">
        {error && (
          <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="bg-white rounded-2xl shadow-lg p-8"
        >
          <div className="mb-6 flex items-center justify-between gap-4">
            <h1 className="text-3xl font-bold text-gray-800">
              Edit item details
            </h1>
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
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Item Name */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Item Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Enter item name"
              />
            </div>

            {/* HSN/SAC */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                HSN/SAC
              </label>
              <input
                type="text"
                name="hsn_sac"
                value={formData.hsn_sac}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Enter HSN/SAC code"
              />
            </div>

            {/* UOM */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Unit of Measure <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="uom"
                value={formData.uom}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="e.g., PCS, KG, L"
              />
            </div>

            {/* Rate */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Rate <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <span className="absolute left-3 top-2 text-gray-600">₹</span>
                <input
                  type="number"
                  name="rate"
                  value={formData.rate}
                  onChange={handleChange}
                  required
                  step="0.01"
                  min="0"
                  className="w-full pl-8 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="0.00"
                />
              </div>
            </div>

            {/* GST Percentage */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                GST % <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <input
                  type="number"
                  name="gst_percentage"
                  value={formData.gst_percentage}
                  onChange={handleChange}
                  required
                  step="0.01"
                  min="0"
                  max="100"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="0.00"
                />
                <span className="absolute right-3 top-2 text-gray-600">%</span>
              </div>
            </div>

            {/* Description */}
            <div className="md:col-span-2">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Description
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                rows="4"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Enter item description"
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4 mt-8 pt-6 border-t border-gray-200">
            <button
              type="submit"
              disabled={saving}
              className="flex-1 flex items-center justify-center gap-2 flex-1 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 disabled:opacity-50 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 shadow-md hover:shadow-lg"
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
      </div>
    </DashboardLayout>
  );
}
