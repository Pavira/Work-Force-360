import { Menu } from "lucide-react";

export default function Navbar({ onMenuToggle }) {
  return (
    <nav className="fixed top-0 left-0 right-0 h-18 bg-gradient-to-r from-purple-600 to-purple-800 flex items-center justify-between px-4 md:px-8 shadow-lg z-50">
      <div className="flex items-center gap-4">
        <button
          onClick={onMenuToggle}
          className="lg:hidden text-white hover:bg-purple-700 p-2 rounded-lg transition"
        >
          <Menu size={28} />
        </button>
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-white text-purple-700 flex items-center justify-center font-bold">
            S
          </div>
          <div>
            <h1 className="text-lg md:text-xl font-bold text-white">
              Work-Force-360-Admin-Panel
            </h1>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-3 md:gap-4">
        <div className="text-right hidden sm:block">
          <p className="text-sm font-semibold text-white">Admin</p>
          <p className="text-xs text-purple-200">admin@workforce360.com</p>
        </div>
        <div className="w-12 h-12 rounded-full bg-white text-purple-700 flex items-center justify-center font-bold text-lg flex-shrink-0">
          A
        </div>
      </div>
    </nav>
  );
}
