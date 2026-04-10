// src/components/Layout.jsx
import React, { useState, useEffect } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";
import useNotificationStore from "../store/notificationStore";
import NotificationIcon from "./NotificationIcon";
import NotificationPanel from "./NotificationPanel";
import logoIbdn from "../assets/logo-ibdn.svg";
import { 
  Menu, X, LogOut, Home, FileText, Star, 
  Building2, Tags, Mailbox, Leaf, Users, 
  UserCircle, ShieldCheck
} from "lucide-react";

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
    `flex items-center px-4 py-2.5 rounded-lg transition-all duration-200 ${
      isActive
        ? "bg-white/20 text-white font-medium shadow-sm translate-x-1"
        : "text-white/80 hover:bg-white/10 hover:text-white"
    }`;

  const sidebarContent = (
    <>
      <div className="h-20 flex items-center justify-center px-6 border-b border-white/10 shrink-0">
        <img src={logoIbdn} alt="IBDN Logo" className="h-10 w-auto filter drop-shadow-md brightness-0 invert" />
      </div>
      <nav className="flex-1 overflow-y-auto p-4 space-y-1.5 custom-scrollbar">
        <NavLink to="/" className={linkClass} end onClick={() => setSidebarOpen(false)}>
          <Home className="w-5 h-5 mr-3" strokeWidth={1.5} />
          Início
        </NavLink>
        {isEmpresa && user.empresa_id && (
          <NavLink to="/meu-cadastro" className={linkClass} onClick={() => setSidebarOpen(false)}>
            <FileText className="w-5 h-5 mr-3" strokeWidth={1.5} />
            Meu Cadastro
          </NavLink>
        )}
        {isEmpresa && !isAdmin && (
          <NavLink to="/solicitar-selo" className={linkClass} onClick={() => setSidebarOpen(false)}>
            <Star className="w-5 h-5 mr-3" strokeWidth={1.5} />
            Solicitar Selo
          </NavLink>
        )}
        {isAdmin && (
          <>
            <div className="pt-4 pb-2">
              <p className="px-4 text-xs font-semibold text-white/50 uppercase tracking-wider">
                Administração
              </p>
            </div>
            <NavLink to="/empresas" className={linkClass} onClick={() => setSidebarOpen(false)}>
              <Building2 className="w-5 h-5 mr-3" strokeWidth={1.5} />
              Empresas
            </NavLink>
            <NavLink to="/tipos-selo" className={linkClass} onClick={() => setSidebarOpen(false)}>
              <Tags className="w-5 h-5 mr-3" strokeWidth={1.5} />
              Gerenciar Selos
            </NavLink>

            <NavLink to="/solicitacoes-selo" className={linkClass} onClick={() => setSidebarOpen(false)}>
              <Mailbox className="w-5 h-5 mr-3" strokeWidth={1.5} />
              Solicitações
            </NavLink>
            <NavLink to="/ramos" className={linkClass} onClick={() => setSidebarOpen(false)}>
              <Leaf className="w-5 h-5 mr-3" strokeWidth={1.5} />
              Ramos
            </NavLink>
            <div className="pt-4 pb-2">
              <p className="px-4 text-xs font-semibold text-white/50 uppercase tracking-wider">
                Acessos
              </p>
            </div>
            <NavLink to="/utilizadores" className={linkClass} onClick={() => setSidebarOpen(false)}>
              <Users className="w-5 h-5 mr-3" strokeWidth={1.5} />
              Utilizadores
            </NavLink>
            <NavLink to="/perfis" className={linkClass} onClick={() => setSidebarOpen(false)}>
              <UserCircle className="w-5 h-5 mr-3" strokeWidth={1.5} />
              Perfis
            </NavLink>
            <NavLink to="/permissoes" className={linkClass} onClick={() => setSidebarOpen(false)}>
              <ShieldCheck className="w-5 h-5 mr-3" strokeWidth={1.5} />
              Permissões
            </NavLink>
          </>
        )}
      </nav>
      <div className="p-4 border-t border-white/10 shrink-0">
        <button
          onClick={handleLogout}
          className="w-full text-left flex items-center px-4 py-2.5 rounded-lg transition-colors text-white/80 hover:bg-white/10 hover:text-white"
        >
          <LogOut className="w-5 h-5 mr-3" strokeWidth={1.5} />
          Sair
        </button>
      </div>
    </>
  );

  return (
    <div className="flex h-screen bg-ibdn-bg font-sans selection:bg-ibdn-primary selection:text-white text-gray-800">
      <aside className="w-72 flex-shrink-0 bg-ibdn-primary text-white flex-col hidden md:flex shadow-xl z-20">
        {sidebarContent}
      </aside>
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-ibdn-primary/40 backdrop-blur-sm z-30 md:hidden transition-opacity"
          onClick={() => setSidebarOpen(false)}
        ></div>
      )}
      <aside
        className={`fixed top-0 left-0 h-full w-72 bg-ibdn-primary text-white flex-col flex z-40 transform transition-transform duration-300 ease-in-out md:hidden shadow-2xl ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {sidebarContent}
      </aside>
      <div className="flex-1 flex flex-col overflow-hidden relative">
        <header className="h-20 bg-white/70 backdrop-blur-md border-b border-gray-200/50 flex items-center justify-between px-8 z-10 sticky top-0 shadow-sm">
          <button
            className="p-2 -ml-2 text-gray-500 hover:text-ibdn-primary md:hidden rounded-lg hover:bg-gray-100 transition-colors"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Abrir menu"
          >
            <Menu className="w-6 h-6" />
          </button>
          <div className="flex items-center">
            {/* Espaço reservado para Breadcrumbs se necessário */}
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-ibdn-primary/10 flex items-center justify-center text-ibdn-primary hidden sm:flex border border-ibdn-primary/20">
                <UserCircle className="w-6 h-6" strokeWidth={1.5}/>
              </div>
              <div className="hidden sm:flex flex-col">
                <span className="text-sm font-semibold text-gray-800">
                  {user.email.split("@")[0] || "Usuário"}
                </span>
                <span className="text-xs text-gray-500 uppercase tracking-wider">
                  {isAdmin ? "Administrador" : "Parceiro"}
                </span>
              </div>
            </div>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-4 md:p-8 bg-ibdn-bg/50">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
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
