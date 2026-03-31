import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import DashboardLayout from "../../app/layout/DashboardLayout";
import { Plus, Search, ChevronLeft, ChevronRight, Eye } from "lucide-react";
import {
  getAllApprovedCompanies,
  getAllDraftCompanies,
  getAllUnApprovedCompanies,
} from "@/services/company_service";
import PageHeader from "@/components/ui/PageHeader";
import StatusFilterSection from "@/components/ui/StatusFilterSection";

export default function ListCompanies() {
  const navigate = useNavigate();
  const [approvedCompanies, setApprovedCompanies] = useState([]);
  const [unApprovedCompanies, setUnApprovedCompanies] = useState([]);
  const [draftCompanies, setDraftCompanies] = useState([]);
  const [approvedCount, setApprovedCount] = useState(0);
  const [unApprovedCount, setUnApprovedCount] = useState(0);
  const [draftCount, setDraftCount] = useState(0);
  const [totalCompanies, setTotalCompanies] = useState(0);
  const [activeStatus, setActiveStatus] = useState("approved");
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [companiesPerPage] = useState(10);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCompanies();
  }, []);

  const fetchCompanies = async () => {
    try {
      setLoading(true);
      setError(null);
      const [approvedResult, unapprovedResult, draftResult] =
        await Promise.allSettled([
          getAllApprovedCompanies(),
          getAllUnApprovedCompanies(),
          getAllDraftCompanies(),
        ]);

      const allFailed =
        approvedResult.status === "rejected" &&
        unapprovedResult.status === "rejected" &&
        draftResult.status === "rejected";

      if (allFailed) {
        throw new Error("All company status APIs failed");
      }

      const getPayload = (result) => {
        if (!result || result.status !== "fulfilled") return {};
        const response = result.value;
        if (response && typeof response === "object" && response.data) {
          return response.data;
        }
        return response || {};
      };

      const approvedPayload = getPayload(approvedResult);
      const unapprovedPayload = getPayload(unapprovedResult);
      const draftPayload = getPayload(draftResult);
      const approvedList = Array.isArray(approvedPayload?.approved_companies)
        ? approvedPayload.approved_companies
        : [];
      const unApprovedList = Array.isArray(
        unapprovedPayload?.unapproved_companies,
      )
        ? unapprovedPayload.unapproved_companies
        : [];
      const draftList = Array.isArray(draftPayload?.draft_companies)
        ? draftPayload.draft_companies
        : [];

      setApprovedCompanies(approvedList);
      setUnApprovedCompanies(unApprovedList);
      setDraftCompanies(draftList);

      const pickFirstFinite = (...values) =>
        values.find((value) => Number.isFinite(value));

      const resolvedApprovedCount = pickFirstFinite(
        approvedPayload?.approved_companies_count,
        unapprovedPayload?.approved_companies_count,
        draftPayload?.approved_companies_count,
        approvedList.length,
      );

      const resolvedUnapprovedCount = pickFirstFinite(
        approvedPayload?.unapproved_companies_count,
        unapprovedPayload?.unapproved_companies_count,
        draftPayload?.unapproved_companies_count,
        unApprovedList.length,
      );

      const resolvedDraftCount = pickFirstFinite(
        approvedPayload?.draft_companies_count,
        unapprovedPayload?.draft_companies_count,
        draftPayload?.draft_companies_count,
        draftList.length,
      );

      const resolvedTotalCompanies = pickFirstFinite(
        approvedPayload?.total_companies_count,
        unapprovedPayload?.total_companies_count,
        draftPayload?.total_companies_count,
        resolvedApprovedCount + resolvedUnapprovedCount + resolvedDraftCount,
      );

      setApprovedCount(resolvedApprovedCount);
      setUnApprovedCount(resolvedUnapprovedCount);
      setDraftCount(resolvedDraftCount);
      setTotalCompanies(resolvedTotalCompanies);
    } catch (err) {
      setError("Failed to load companies");
      console.error("Error fetching companies:", err);
    } finally {
      setLoading(false);
    }
  };

  const companiesByStatus =
    activeStatus === "approved"
      ? approvedCompanies
      : activeStatus === "unapproved"
        ? unApprovedCompanies
        : draftCompanies;

  const filteredCompanies = companiesByStatus.filter((company) => {
    const query = searchTerm.toLowerCase();
    return (
      (company.company_name || "").toLowerCase().includes(query) ||
      (company.industry_name || "").toLowerCase().includes(query) ||
      (company.contact_person_name || "").toLowerCase().includes(query) ||
      (company.status || "").toLowerCase().includes(query)
    );
  });

  const totalPages = Math.ceil(filteredCompanies.length / companiesPerPage);
  const startIndex = (currentPage - 1) * companiesPerPage;
  const paginatedCompanies = filteredCompanies.slice(
    startIndex,
    startIndex + companiesPerPage,
  );

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

  const statusOptions = [
    { value: "approved", label: "Approved", count: approvedCount },
    { value: "unapproved", label: "Un-Approved", count: unApprovedCount },
    { value: "draft", label: "Draft", count: draftCount },
  ];

  return (
    <DashboardLayout>
      {/* Header section */}
      <div className="bg-white rounded-2xl shadow-lg p-4 md:p-6">
        <PageHeader
          title="Companies Management"
          subtitle="Manage your com panies"
          action={
            <button
              onClick={() => navigate("/customers/add")}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white text-sm md:text-base font-semibold py-2 md:py-2.5 px-3 md:px-4 rounded-lg transition duration-200 shadow-md hover:shadow-lg"
            >
              <Plus size={18} />
              Add Companies
            </button>
          }
        />

        {/* Status Filter */}
        <StatusFilterSection
          summaryLabel="Total Companies"
          summaryCount={totalCompanies}
          options={statusOptions}
          activeValue={activeStatus}
          onChange={(value) => {
            setActiveStatus(value);
            setCurrentPage(1);
          }}
        />

        {/* Search Bar */}
        <div className="mb-6 relative">
          <Search className="absolute left-3 top-3 text-gray-400" size={20} />
          <input
            type="text"
            placeholder={`Search ${activeStatus === "approved" ? "approved" : activeStatus === "unapproved" ? "un-approved" : "draft"} companies...`}
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setCurrentPage(1);
            }}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
          </div>
        ) : paginatedCompanies.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No companies found</p>
            <p className="text-gray-400 mt-2">
              {searchTerm
                ? "Try adjusting your search"
                : "Add your first company to get started"}
            </p>
          </div>
        ) : (
          <>
            <div className="hidden md:block overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200 bg-gray-50">
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                      Company Name
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                      Industry Name
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                      Contact Person Name
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                      Status
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {paginatedCompanies.map((company) => (
                    <tr
                      key={company.id}
                      onClick={() => navigate(`/companies/${company.id}`)}
                      className="border-b border-gray-200 hover:bg-gray-50 transition duration-150 cursor-pointer"
                    >
                      <td className="px-6 py-4 text-sm text-gray-800 font-medium">
                        {company.company_name || "-"}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {company.industry_name || "-"}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {company.contact_person_name || "-"}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {company.status || "-"}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/companies/${company.id}`);
                          }}
                          className="text-purple-600 hover:text-purple-800"
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
              {paginatedCompanies.map((company) => (
                <div
                  key={company.id}
                  onClick={() => navigate(`/companies/${company.id}`)}
                  className="bg-gray-50 rounded-2xl border border-gray-200 p-5 space-y-2 cursor-pointer hover:bg-gray-100 transition duration-150"
                >
                  <h3 className="font-semibold text-gray-800">
                    {company.company_name || "-"}
                  </h3>
                  <p className="text-sm text-gray-600">
                    Industry: {company.industry_name || "-"}
                  </p>
                  <p className="text-sm text-gray-600">
                    Contact Person: {company.contact_person_name || "-"}
                  </p>
                  <p className="text-sm text-gray-600">
                    Status: {company.status || "-"}
                  </p>
                  <div className="flex justify-end">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate(`/companies/${company.id}`);
                      }}
                      className="text-purple-600 hover:text-purple-800"
                    >
                      <Eye size={18} />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mt-6 pt-4 border-t border-gray-200">
              <div className="text-xs md:text-sm text-gray-600">
                Showing {startIndex + 1} to{" "}
                {Math.min(
                  startIndex + companiesPerPage,
                  filteredCompanies.length,
                )}{" "}
                of {filteredCompanies.length} companies
              </div>

              {/* Pagination */}
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
                  disabled={currentPage === totalPages || totalPages === 0}
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
