import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import DashboardLayout from "../../app/layout/DashboardLayout";
import { Plus, Eye, Search, ChevronLeft, ChevronRight } from "lucide-react";
import { getAllItems } from "@/services/items_service";
import PageHeader from "@/components/ui/PageHeader";

export default function ListItems() {
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getAllItems();
      setItems(response.items || []);
    } catch (err) {
      setError("Failed to load items");
      console.error("Error fetching items:", err);
    } finally {
      setLoading(false);
    }
  };

  // Filter items based on search term
  const filteredItems = items.filter(
    (item) =>
      item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (item.hsn_sac &&
        item.hsn_sac.toLowerCase().includes(searchTerm.toLowerCase())),
  );

  // Pagination logic
  const totalPages = Math.ceil(filteredItems.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedItems = filteredItems.slice(
    startIndex,
    startIndex + itemsPerPage,
  );

  const handleRowClick = (itemId) => {
    navigate(`/items/${itemId}`);
  };

  const handleEyeClick = (itemId) => {
    navigate(`/items/${itemId}`);
  };

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  return (
    <DashboardLayout>
      <div className="bg-white rounded-2xl shadow-lg p-4 md:p-6">
        <PageHeader
          title="Items Management"
          subtitle="Manage your inventory items"
          action={
            <button
              onClick={() => navigate("/items/add")}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white text-sm md:text-base font-semibold py-2 md:py-2.5 px-3 md:px-4 rounded-lg transition duration-200 shadow-md hover:shadow-lg"
            >
              <Plus size={18} />
              Add Item
            </button>
          }
        />

        {/* Search Bar */}
        <div className="mb-6 relative">
          <Search className="absolute left-3 top-3 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Search by item name or HSN/SAC..."
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setCurrentPage(1);
            }}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* Loading State */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
          </div>
        ) : paginatedItems.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No items found</p>
            <p className="text-gray-400 mt-2">
              {searchTerm
                ? "Try adjusting your search"
                : "Add your first item to get started"}
            </p>
          </div>
        ) : (
          <>
            {/* Table */}
            <div className="hidden md:block overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200 bg-gray-50">
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                      Item Name
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                      HSN/SAC
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                      UOM
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                      Rate
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                      GST %
                    </th>
                    <th className="px-6 py-4 text-center text-sm font-semibold text-gray-700">
                      Action
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {paginatedItems.map((item) => (
                    <tr
                      key={item.id}
                      className="border-b border-gray-200 hover:bg-gray-50 cursor-pointer transition duration-150"
                      onClick={() => handleRowClick(item.id)}
                    >
                      <td className="px-6 py-4 text-sm text-gray-800 font-medium">
                        {item.name}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {item.hsn_sac || "—"}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {item.uom}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        ₹{parseFloat(item.rate).toFixed(2)}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {item.gst_percentage}%
                      </td>
                      <td className="px-6 py-4 text-center">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleEyeClick(item.id);
                          }}
                          className="inline-flex items-center justify-center w-10 h-10 rounded-lg bg-purple-100 text-purple-600 hover:bg-purple-200 transition duration-150"
                          title="View Item"
                        >
                          <Eye size={18} />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Mobile Cards */}
            <div className="md:hidden space-y-4">
              {paginatedItems.map((item) => (
                <div
                  key={item.id}
                  className="bg-gray-50 rounded-2xl border border-gray-200 p-5 space-y-2"
                  onClick={() => handleRowClick(item.id)}
                >
                  <div className="flex justify-between items-start gap-3">
                    <h3 className="font-semibold text-gray-800">
                      {item.name || "-"}
                    </h3>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleEyeClick(item.id);
                      }}
                      className="text-purple-600 text-sm hover:underline flex items-center gap-1"
                    >
                      <Eye size={14} />
                      View
                    </button>
                  </div>
                  <p className="text-sm text-gray-600">
                    HSN/SAC: {item.hsn_sac || "-"}
                  </p>
                  <p className="text-sm text-gray-600">UOM: {item.uom || "-"}</p>
                  <p className="text-sm text-gray-600">
                    Rate: Rs. {Number(item.rate || 0).toFixed(2)}
                  </p>
                  <p className="text-sm text-gray-600">
                    GST: {item.gst_percentage || 0}%
                  </p>
                </div>
              ))}
            </div>

            {/* Pagination */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mt-6 pt-4 border-t border-gray-200">
              <div className="text-xs md:text-sm text-gray-600">
                Showing {startIndex + 1} to{" "}
                {Math.min(startIndex + itemsPerPage, filteredItems.length)} of{" "}
                {filteredItems.length} items
              </div>

              <div className="flex items-center gap-1 md:gap-2">
                <button
                  onClick={handlePrevPage}
                  disabled={currentPage === 1}
                  className="flex items-center gap-1 px-2 md:px-3 py-1.5 md:py-2 rounded-lg border border-gray-300 text-xs md:text-sm text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition duration-150"
                >
                  <ChevronLeft size={14} />
                  Previous
                </button>

                <div className="hidden sm:flex items-center gap-1">
                  {Array.from({ length: totalPages }, (_, i) => i + 1).map(
                    (page) => (
                      <button
                        key={page}
                        onClick={() => setCurrentPage(page)}
                        className={`w-8 h-8 md:w-10 md:h-10 text-xs md:text-sm rounded-lg font-medium transition duration-150 ${
                          currentPage === page
                            ? "bg-purple-600 text-white"
                            : "border border-gray-300 text-gray-700 hover:bg-gray-50"
                        }`}
                      >
                        {page}
                      </button>
                    ),
                  )}
                </div>

                <button
                  onClick={handleNextPage}
                  disabled={currentPage === totalPages}
                  className="flex items-center gap-1 px-2 md:px-3 py-1.5 md:py-2 rounded-lg border border-gray-300 text-xs md:text-sm text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition duration-150"
                >
                  Next
                  <ChevronRight size={14} />
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  );
}
