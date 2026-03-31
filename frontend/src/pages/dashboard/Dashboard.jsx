import { useEffect, useState } from "react";
import DashboardLayout from "../../app/layout/DashboardLayout";
import StatCard from "../../components/ui/StatCard";
import { getDashboardStats } from "@/services/dashboard_service";
import erp1Image from "@/assets/erp1.jpg";

export default function Dashboard() {
  const [isLoadingStats, setIsLoadingStats] = useState(true);
  const [stats, setStats] = useState({
    total_invoices: 0,
    total_customers: 0,
    total_items: 0,
    total_revenue: 0,
  });

  useEffect(() => {
    const fetchDashboardStats = async () => {
      setIsLoadingStats(true);
      try {
        const res = await getDashboardStats();
        if (res?.success && res?.data) {
          setStats(res.data);
        }
      } catch (error) {
        console.error("Failed to fetch dashboard stats:", error);
      } finally {
        setIsLoadingStats(false);
      }
    };

    fetchDashboardStats();
  }, []);

  return (
    <DashboardLayout>
      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8 md:mb-10">
        <StatCard
          title="Total Invoices"
          value={stats.total_invoices}
          isLoading={isLoadingStats}
        />
        <StatCard
          title="Customers"
          value={stats.total_customers}
          isLoading={isLoadingStats}
        />
        <StatCard title="Items" value={stats.total_items} isLoading={isLoadingStats} />
        <StatCard
          title="Total Revenue"
          value={stats.total_revenue}
          isLoading={isLoadingStats}
        />
      </div>

      {/* ERP Section */}
      <div className="bg-white rounded-2xl shadow p-4 md:p-6 mt-6">
        <h3 className="text-base md:text-lg font-semibold mb-4">ERP</h3>
        <img
          src={erp1Image}
          alt="ERP"
          className="w-full h-[360px] object-contain rounded-xl bg-white"
        />
      </div>
    </DashboardLayout>
  );
}
