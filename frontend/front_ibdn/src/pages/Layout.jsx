import React, { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";

// --- Ícones em SVG para um design mais limpo ---
const MenuIcon = (props) => (
  <svg {...props} stroke="currentColor" fill="none" viewBox="0 0 24 24">
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M4 6h16M4 12h16m-7 6h7"
    />
  </svg>
);

const LogoutIcon = (props) => (
  <svg {...props} stroke="currentColor" fill="none" viewBox="0 0 24 24">
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
    />
  </svg>
);

function Layout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const navigate = useNavigate();
  const logout = useAuthStore((state) => state.logout);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const linkClass = ({ isActive }) =>
    `flex items-center px-4 py-2 rounded-md transition-colors ${
      isActive
        ? "bg-gray-700 text-white"
        : "text-gray-400 hover:bg-gray-700 hover:text-white"
    }`;

  const sidebarContent = (
    <>
      <div className="h-16 flex items-center justify-center text-2xl font-bold">
        IBDN Painel
      </div>
      <nav className="flex-grow p-4 space-y-2">
        <NavLink to="/" className={linkClass}>
          <span className="mr-3">🏠</span>
          Início
        </NavLink>
        <NavLink to="/empresas" className={linkClass}>
          <span className="mr-3">🏢</span>
          Empresas
        </NavLink>
        {/* Adicione outros links aqui */}
      </nav>
      <div className="p-4 border-t border-gray-700">
        <button
          onClick={handleLogout}
          className="w-full text-left flex items-center px-4 py-2 rounded-md transition-colors text-gray-400 hover:bg-gray-700 hover:text-white"
        >
          <LogoutIcon className="w-5 h-5 mr-3" />
          Sair
        </button>
      </div>
    </>
  );

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar para telas maiores (desktop) */}
      <aside className="w-64 flex-shrink-0 bg-gray-800 text-white flex-col hidden md:flex">
        {sidebarContent}
      </aside>

      {/* Overlay para fechar sidebar no mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black opacity-50 z-20 md:hidden"
          onClick={() => setSidebarOpen(false)}
        ></div>
      )}

      {/* Sidebar para telas menores (mobile) */}
      <aside
        className={`fixed top-0 left-0 h-full w-64 bg-gray-800 text-white flex-col flex z-30 transform transition-transform duration-300 ease-in-out md:hidden ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {sidebarContent}
      </aside>

      {/* Conteúdo Principal */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
          {/* Botão Hambúrguer para abrir menu no mobile */}
          <button
            className="text-gray-500 hover:text-gray-700 md:hidden"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            <MenuIcon className="w-6 h-6" />
          </button>

          <h1 className="text-xl font-semibold text-gray-800">Dashboard</h1>

          <div className="flex items-center">
            <p className="text-gray-600 hidden sm:block">Bem-vindo, Usuário!</p>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>
    </div>
  );
}

export default Layout;
