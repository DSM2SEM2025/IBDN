// src/components/Layout.jsx
import React, { useState, useEffect } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";
import useNotificationStore from "../store/notificationStore";
import NotificationIcon from "./NotificationIcon";
import NotificationPanel from "./NotificationPanel";

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
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  const fetchNotifications = useNotificationStore(
    (state) => state.fetchNotifications
  );

  useEffect(() => {
    if (user?.permissoes.includes("empresa") && user.empresa_id) {
      fetchNotifications(user.empresa_id);
    }
  }, [user, fetchNotifications]);

  if (!user) {
    return null;
  }

  const isAdmin =
    user.permissoes.includes("admin") ||
    user.permissoes.includes("admin_master");

  const isEmpresa = user.permissoes.includes("empresa");

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const linkClass = ({ isActive }) =>
    `flex items-center px-4 py-2 rounded-md transition-colors ${
      isActive
        ? "bg-gray-700 text-white"
        : "text-white hover:bg-gray-700 hover:text-white"
    }`;

  const sidebarContent = (
    <>
      <div className="h-16 flex items-center justify-center text-white text-2xl font-bold">
        IBDN Painel
      </div>
      <nav className="flex-grow p-4 space-y-2">
        <NavLink to="/" className={linkClass} end>
          <span className="mr-3">🏠</span>
          Início
        </NavLink>
        {isEmpresa && user.empresa_id && (
          <NavLink to="/meu-cadastro" className={linkClass}>
            <span className="mr-3">📄</span>
            Meu Cadastro
          </NavLink>
        )}
        {isEmpresa && !isAdmin && (
          <NavLink to="/solicitar-selo" className={linkClass}>
            <span className="mr-3">⭐</span>
            Solicitar Selo
          </NavLink>
        )}
        {isAdmin && (
          <>
            <hr className="my-2 border-gray-700" />
            <NavLink to="/empresas" className={linkClass}>
              <span className="mr-3">🏢</span>
              Empresas
            </NavLink>
            <NavLink to="/tipos-selo" className={linkClass}>
              <span className="mr-3">🏷️</span>
              Gerenciar Selos
            </NavLink>

            <NavLink to="/solicitacoes-selo" className={linkClass}>
              <span className="mr-3">📬</span>
              Solicitações
            </NavLink>
            <NavLink to="/ramos" className={linkClass}>
              <span className="mr-3">🌿</span>
              Ramos
            </NavLink>
            <hr className="my-2 border-gray-600" />
            <NavLink to="/utilizadores" className={linkClass}>
              <span className="mr-3">👤</span>
              Utilizadores
            </NavLink>
            <NavLink to="/perfis" className={linkClass}>
              <span className="mr-3">👥</span>
              Perfis
            </NavLink>
            <NavLink to="/permissoes" className={linkClass}>
              <span className="mr-3">🛡️</span>
              Permissões
            </NavLink>
          </>
        )}
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
      <aside className="w-64 flex-shrink-0 bg-green-900 text-white flex-col hidden md:flex">
        {sidebarContent}
      </aside>
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black opacity-50 z-20 md:hidden"
          onClick={() => setSidebarOpen(false)}
        ></div>
      )}
      <aside
        className={`fixed top-0 left-0 h-full w-64 bg-gray-800 text-white flex-col flex z-30 transform transition-transform duration-300 ease-in-out md:hidden ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {sidebarContent}
      </aside>
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
          <button
            className="text-gray-500 hover:text-gray-700 md:hidden"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            <MenuIcon className="w-6 h-6" />
          </button>
          <div className="flex items-center"></div>
          <div className="flex items-center">
            <p className="text-gray-600 hidden sm:block">
              Bem-vindo, {user.email}!
            </p>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>

      {/* Componentes do sistema de notificação global */}
      {isEmpresa && !isAdmin && (
        <>
          <NotificationIcon />
          <NotificationPanel />
        </>
      )}
    </div>
  );
}

export default Layout;
