import { useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  FileText,
  Users,
  Package,
  LogOut,
  X,
} from "lucide-react";

export default function Sidebar({ isOpen, onClose }) {
  const navigate = useNavigate();

  const menu = [
    {
      name: "Dashboard",
      icon: <LayoutDashboard size={18} />,
      path: "/dashboard",
    },
    // { name: "Invoices", icon: <FileText size={18} />, path: "/invoices" },
    { name: "Companies", icon: <Users size={18} />, path: "/companies" },
    // { name: "Items", icon: <Package size={18} />, path: "/items" },
  ];

  const logoutMenu = [
    { name: "Logout", icon: <LogOut size={18} />, path: "/logout" },
  ];

  const handleMenuClick = (path) => {
    navigate(path);
    onClose();
  };

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-opacity-50 z-30 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed lg:static top-18 left-0 w-64 bg-gradient-to-b from-purple-700 to-purple-900 text-white h-[calc(100vh-80px)] lg:h-screen lg:flex lg:flex-col px-6 py-6 z-40 transform transition-transform duration-300 ease-in-out overflow-y-auto ${
          isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        }`}
      >
        {/* Close button for mobile */}
        <button
          onClick={onClose}
          className="lg:hidden absolute top-6 right-6 text-white hover:bg-purple-600 p-2 rounded-lg"
        >
          <X size={24} />
        </button>

        <ul className="space-y-2">
          {menu.map((item) => (
            <li
              key={item.name}
              className="flex items-center gap-3 px-4 py-3 rounded-xl cursor-pointer hover:bg-purple-600 transition duration-200"
              onClick={() => handleMenuClick(item.path)}
            >
              {item.icon}
              <span className="text-sm lg:text-base">{item.name}</span>
            </li>
          ))}
        </ul>

        <div className="mt-auto pt-4 border-t border-purple-600">
          <ul className="space-y-2">
            {logoutMenu.map((item) => (
              <li
                key={item.name}
                className="flex items-center gap-3 px-4 py-3 rounded-xl cursor-pointer hover:bg-purple-600 transition duration-200"
                onClick={() => handleMenuClick(item.path)}
              >
                {item.icon}
                <span className="text-sm lg:text-base">{item.name}</span>
              </li>
            ))}
          </ul>
        </div>
      </aside>
    </>
  );
}
