import { useState } from "react";
import Navbar from "../../components/navbar/Navbar";
import Sidebar from "../../components/sidebar/Sidebar";
import { Toaster } from "react-hot-toast";

export default function DashboardLayout({ children }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);
  const closeSidebar = () => setIsSidebarOpen(false);

  return (
    <div className="bg-gray-100 min-h-screen">
      <Navbar onMenuToggle={toggleSidebar} />
      <Toaster position="top-right" />

      <div className="flex pt-15">
        <Sidebar isOpen={isSidebarOpen} onClose={closeSidebar} />

        <main className="flex-1 overflow-auto p-4 md:p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
