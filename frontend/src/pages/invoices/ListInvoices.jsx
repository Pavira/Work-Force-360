import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import DashboardLayout from "../../app/layout/DashboardLayout";
import {
  Plus,
  Eye,
  Search,
  ChevronLeft,
  ChevronRight,
  X,
  Printer,
  Download,
} from "lucide-react";
import { getAllInvoices } from "@/services/invoice_service";

export default function ListInvoices() {
  const navigate = useNavigate();
  const apiBaseUrl = import.meta.env.VITE_API_URL || "";
  const [invoices, setInvoices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [perPage] = useState(10);
  const [showModal, setShowModal] = useState(false);
  const [selectedInvoice, setSelectedInvoice] = useState(null);

  useEffect(() => {
    fetchInvoices();
  }, []);

  const fetchInvoices = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getAllInvoices();
      setInvoices(response.invoices || []);
    } catch (err) {
      setError("Failed to load invoices");
      console.error("Error fetching invoices:", err);
    } finally {
      setLoading(false);
    }
  };

  const filtered = invoices.filter((inv) => {
    const q = searchTerm.toLowerCase();
    return (
      (inv.invoice_number &&
        inv.invoice_number.toString().toLowerCase().includes(q)) ||
      (inv.po_number && inv.po_number.toString().toLowerCase().includes(q)) ||
      (inv.consignee?.name &&
        inv.consignee.name.toString().toLowerCase().includes(q)) ||
      (inv.buyer?.name && inv.buyer.name.toString().toLowerCase().includes(q))
    );
  });

  const totalPages = Math.max(1, Math.ceil(filtered.length / perPage));
  const startIndex = (currentPage - 1) * perPage;
  const paginated = filtered.slice(startIndex, startIndex + perPage);

  const handleRowClick = (id) => navigate(`/invoices/${id}`);

  const handleViewInvoice = (invoice) => {
    setSelectedInvoice(invoice);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedInvoice(null);
  };

  const getDownloadDatePart = (invoice) => {
    const rawDate =
      invoice?.created_date || invoice?.created_at || invoice?.invoice_date;
    if (!rawDate) return "unknown-date";

    const parsed = new Date(rawDate);
    if (Number.isNaN(parsed.getTime())) {
      return String(rawDate).replace(/[^\w-]/g, "-");
    }

    const yyyy = parsed.getFullYear();
    const mm = String(parsed.getMonth() + 1).padStart(2, "0");
    const dd = String(parsed.getDate()).padStart(2, "0");
    return `${yyyy}-${mm}-${dd}`;
  };

  const handlePrint = async () => {
    if (!selectedInvoice?.id) {
      console.error("Invoice ID not available");
      return;
    }

    try {
      const invoiceUrl = apiBaseUrl
        ? `/SPM_bill.html?invoice_id=${selectedInvoice.id}&api_base=${encodeURIComponent(
            apiBaseUrl,
          )}&print=1`
        : `/SPM_bill.html?invoice_id=${selectedInvoice.id}&print=1`;
      window.open(invoiceUrl, "_blank", "noopener");
    } catch (error) {
      console.error("Error opening invoice for printing:", error);
    }
  };

  const handleDownload = async () => {
    if (!selectedInvoice?.id) {
      console.error("Invoice ID not available");
      return;
    }

    try {
      const baseApi = (import.meta.env.VITE_API_URL || "/api/v1").replace(
        /\/$/,
        "",
      );
      const pdfUrl = `${baseApi}/invoices/${selectedInvoice.id}/pdf?download=1`;
      const invoicePart = String(
        selectedInvoice.invoice_number || "invoice",
      ).replace(/[^\w-]/g, "-");
      const datePart = getDownloadDatePart(selectedInvoice);
      const filename = `${invoicePart}-${datePart}.pdf`;

      const link = document.createElement("a");
      link.href = pdfUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error("Error downloading PDF:", error);
    }
  };

  return (
    <DashboardLayout>
      {/* <div className="bg-white rounded-2xl shadow-lg p-8 mb-6"> */}
      <div className="bg-white rounded-2xl shadow-lg p-4 md:p-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6 md:mb-8">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-gray-800">
              Invoices
            </h1>
            <p className="text-sm md:text-base text-gray-500 mt-1">
              Manage your invoices
            </p>
          </div>
          <button
            onClick={() => navigate("/invoices/add")}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white text-sm md:text-base font-semibold py-2 md:py-2.5 px-3 md:px-4 rounded-lg transition duration-200 shadow-md hover:shadow-lg"
          >
            <Plus size={18} />
            Add Invoice
          </button>
        </div>

        {/* Search */}
        <div className="mb-6 relative">
          <Search className="absolute left-3 top-3 text-gray-400" size={18} />
          <input
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setCurrentPage(1);
            }}
            type="text"
            placeholder="Search by invoice, PO, consignee or buyer..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
        </div>

        {/* <div className="bg-white rounded-2xl shadow overflow-hidden"> */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
          </div>
        ) : error ? (
          <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg m-4">
            {error}
          </div>
        ) : paginated.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No invoices found</p>
            <p className="text-gray-400 mt-2">
              {searchTerm
                ? "Try adjusting your search"
                : "Add your first invoice to get started"}
            </p>
          </div>
        ) : (
          <>
            <div className="hidden md:block overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 text-gray-700">
                  <tr>
                    <th className="px-6 py-4 text-left font-semibold">
                      Invoice No
                    </th>
                    <th className="px-6 py-4 text-left font-semibold">
                      PO Number
                    </th>
                    <th className="px-6 py-4 text-left font-semibold">
                      Consignee
                    </th>
                    <th className="px-6 py-4 text-left font-semibold">Buyer</th>
                    <th className="px-6 py-4 text-left font-semibold">
                      Invoice Date
                    </th>
                    <th className="px-6 py-4 text-left font-semibold">
                      Total Amount
                    </th>
                    <th className="px-6 py-4 text-center font-semibold">
                      Action
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {paginated.map((inv) => (
                    <tr
                      key={inv.id}
                      className="border-b border-gray-200 hover:bg-gray-50 cursor-pointer transition duration-150"
                      onClick={() => handleRowClick(inv.id)}
                    >
                      <td className="px-6 py-4 font-medium text-gray-800">
                        {inv.invoice_number}
                      </td>
                      <td className="px-6 py-4 text-gray-600">
                        {inv.po_number || "—"}
                      </td>
                      <td className="px-6 py-4 text-gray-600">
                        {/* consignee name is insder consignee object */}
                        {inv.consignee.name || "—"}
                      </td>
                      <td className="px-6 py-4 text-gray-600">
                        {inv.buyer.name || "—"}
                      </td>
                      <td className="px-6 py-4 text-gray-600">
                        {inv.invoice_date}
                      </td>
                      <td className="px-6 py-4 text-purple-700 font-semibold">
                        ₹{inv.totals.total}
                      </td>
                      <td className="px-6 py-4 text-center">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleViewInvoice(inv);
                          }}
                          className="inline-flex items-center justify-center w-10 h-10 rounded-lg bg-purple-100 text-purple-600 hover:bg-purple-200 transition duration-150"
                          title="View Invoice"
                        >
                          <Eye size={18} />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="md:hidden space-y-4">
              {paginated.map((inv) => (
                <div
                  key={inv.id}
                  className="bg-gray-50 rounded-2xl border border-gray-200 p-5 space-y-2"
                  onClick={() => handleRowClick(inv.id)}
                >
                  <div className="flex justify-between items-center">
                    <h3 className="font-semibold text-gray-800">
                      {inv.invoice_number || "-"}
                    </h3>
                    <span className="text-sm text-gray-500">
                      {inv.invoice_date || "-"}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600">
                    PO: {inv.po_number || "-"}
                  </p>
                  <p className="text-sm text-gray-600">
                    Consignee: {inv.consignee?.name || "-"}
                  </p>
                  <p className="text-sm text-gray-600">
                    Buyer: {inv.buyer?.name || "-"}
                  </p>
                  <div className="flex justify-between items-center pt-2">
                    <span className="font-bold text-purple-700">
                      Rs. {inv.totals?.total ?? 0}
                    </span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleViewInvoice(inv);
                      }}
                      className="text-purple-600 text-sm hover:underline flex items-center gap-1"
                    >
                      <Eye size={14} />
                      View
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Pagination */}
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mt-6 pt-4 border-t border-gray-200">
              <div className="text-xs md:text-sm text-gray-600">
                Showing {startIndex + 1} to{" "}
                {Math.min(startIndex + perPage, filtered.length)} of{" "}
                {filtered.length} invoices
              </div>

              <div className="flex items-center gap-1 md:gap-2">
                <button
                  onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
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
                  onClick={() =>
                    setCurrentPage((p) => Math.min(totalPages, p + 1))
                  }
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
        {/* </div> */}
      </div>

      {/* Invoice Modal */}
      {showModal && selectedInvoice && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            {/* Modal Header */}
            <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-800">
                Invoice Details
              </h2>
              <button
                onClick={closeModal}
                className="text-gray-400 hover:text-gray-600 transition"
              >
                <X size={24} />
              </button>
            </div>

            {/* Modal Content */}
            <div className="p-6">
              {/* <div
                id="invoice-print-content"
                className="bg-gray-50 rounded-lg p-4"
              >
                <InvoiceTemplate invoiceData={selectedInvoice} />
              </div> */}
              <iframe
                src={
                  apiBaseUrl
                    ? `/SPM_bill.html?invoice_id=${selectedInvoice.id}&api_base=${encodeURIComponent(
                        apiBaseUrl,
                      )}`
                    : `/SPM_bill.html?invoice_id=${selectedInvoice.id}`
                }
                title="Invoice Preview"
                className="w-full h-[75vh] border rounded-lg bg-white"
              />
            </div>

            {/* Modal Footer */}
            <div className="bg-gray-50 border-t border-gray-200 px-6 py-4 flex justify-end gap-3">
              <button
                onClick={handlePrint}
                className="flex items-center gap-2 px-4 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 transition"
              >
                <Printer size={18} />
                Print
              </button>
              <button
                onClick={handleDownload}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-purple-600 text-white hover:bg-purple-700 transition"
              >
                <Download size={18} />
                Download
              </button>
            </div>
          </div>
        </div>
      )}
    </DashboardLayout>
  );
}
