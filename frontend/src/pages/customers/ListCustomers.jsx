import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import DashboardLayout from "../../app/layout/DashboardLayout";
import { Plus, Eye, Search, ChevronLeft, ChevronRight } from "lucide-react";
import { getAllCustomers } from "@/services/customer_service";

export default function ListCustomers() {
  const navigate = useNavigate();
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [customersPerPage] = useState(10);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getAllCustomers();
      setCustomers(response.customers || []);
    } catch (err) {
      setError("Failed to load customers");
      console.error("Error fetching customers:", err);
    } finally {
      setLoading(false);
    }
  };

  // Filter customers based on search term
  const filteredCustomers = customers.filter(
    (customer) =>
      customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (customer.email &&
        customer.email.toLowerCase().includes(searchTerm.toLowerCase())),
  );

  // Pagination logic
  const totalPages = Math.ceil(filteredCustomers.length / customersPerPage);
  const startIndex = (currentPage - 1) * customersPerPage;
  const paginatedCustomers = filteredCustomers.slice(
    startIndex,
    startIndex + customersPerPage,
  );

  const handleRowClick = (customerId) => {
    navigate(`/customers/${customerId}`);
  };

  const handleEyeClick = (customerId) => {
    navigate(`/customers/${customerId}`);
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
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6 md:mb-8">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-gray-800">
              Customers Management
            </h1>
            <p className="text-sm md:text-base text-gray-500 mt-1">
              Manage your customers
            </p>
          </div>
          <button
            onClick={() => navigate("/customers/add")}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white text-sm md:text-base font-semibold py-2 md:py-2.5 px-3 md:px-4 rounded-lg transition duration-200 shadow-md hover:shadow-lg"
          >
            <Plus size={18} />
            Add Customer
          </button>
        </div>

        {/* Search Bar */}
        <div className="mb-6 relative">
          <Search className="absolute left-3 top-3 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Search by customer name or email..."
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
        ) : paginatedCustomers.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No customers found</p>
            <p className="text-gray-400 mt-2">
              {searchTerm
                ? "Try adjusting your search"
                : "Add your first customer to get started"}
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
                      Customer Name
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                      Email
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                      Phone Number
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                      GST
                    </th>
                    <th className="px-6 py-4 text-center text-sm font-semibold text-gray-700">
                      Action
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {paginatedCustomers.map((customer) => (
                    <tr
                      key={customer.id}
                      className="border-b border-gray-200 hover:bg-gray-50 cursor-pointer transition duration-150"
                      onClick={() => handleRowClick(customer.id)}
                    >
                      <td className="px-6 py-4 text-sm text-gray-800 font-medium">
                        {/* Show only 20 characters */}
                        {customer.name.length > 20
                          ? `${customer.name.substring(0, 20)}...`
                          : customer.name}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {customer.email || "—"}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {customer.phone || "—"}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {customer.gstin || "—"}
                      </td>
                      <td className="px-6 py-4 text-center">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleEyeClick(customer.id);
                          }}
                          className="inline-flex items-center justify-center w-10 h-10 rounded-lg bg-purple-100 text-purple-600 hover:bg-purple-200 transition duration-150"
                          title="View Customer"
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
              {paginatedCustomers.map((customer) => (
                <div
                  key={customer.id}
                  className="bg-gray-50 rounded-2xl border border-gray-200 p-5 space-y-2"
                  onClick={() => handleRowClick(customer.id)}
                >
                  <div className="flex justify-between items-start gap-3">
                    <h3 className="font-semibold text-gray-800">
                      {customer.name || "-"}
                    </h3>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleEyeClick(customer.id);
                      }}
                      className="text-purple-600 text-sm hover:underline flex items-center gap-1"
                    >
                      <Eye size={14} />
                      View
                    </button>
                  </div>
                  <p className="text-sm text-gray-600">
                    Email: {customer.email || "-"}
                  </p>
                  <p className="text-sm text-gray-600">
                    Phone: {customer.phone || "-"}
                  </p>
                  <p className="text-sm text-gray-600">
                    GST: {customer.gstin || "-"}
                  </p>
                </div>
              ))}
            </div>

            {/* Pagination */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mt-6 pt-4 border-t border-gray-200">
              <div className="text-xs md:text-sm text-gray-600">
                Showing {startIndex + 1} to{" "}
                {Math.min(
                  startIndex + customersPerPage,
                  filteredCustomers.length,
                )}{" "}
                of {filteredCustomers.length} customers
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
