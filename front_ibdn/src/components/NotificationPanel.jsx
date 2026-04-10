import React from "react";
import { X, Bell } from "lucide-react";
import useNotificationStore from "../store/notificationStore";
import NotificacoesList from "./NotificacoesList";

function NotificationPanel() {
  const { isPanelOpen, notifications, markAsRead, closePanel } =
    useNotificationStore();

  if (!isPanelOpen) return null;

  const unreadCount = notifications.filter((n) => !n.lida).length;

  return (
    <>
      {/* Overlay com backdrop-blur */}
      <div
        className="fixed inset-0 bg-black/40 backdrop-blur-sm z-40 transition-all"
        onClick={closePanel}
      />
      {/* Painel lateral */}
      <div className="fixed top-0 right-0 h-full w-full max-w-sm bg-white shadow-2xl z-50 flex flex-col border-l border-gray-100">
        {/* Cabeçalho */}
        <div className="flex justify-between items-center px-6 py-5 border-b border-gray-100 bg-ibdn-bg/30 shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-full bg-ibdn-primary/10 flex items-center justify-center">
              <Bell className="w-5 h-5 text-ibdn-primary" strokeWidth={1.5} />
            </div>
            <div>
              <h3 className="text-xl font-bold font-serif text-ibdn-earthy">
                Notificações
              </h3>
              {unreadCount > 0 && (
                <p className="text-xs text-ibdn-primary font-medium">
                  {unreadCount} não {unreadCount === 1 ? "lida" : "lidas"}
                </p>
              )}
            </div>
          </div>
          <button
            onClick={closePanel}
            className="text-gray-400 bg-transparent hover:bg-gray-100 hover:text-red-500 rounded-full p-2 inline-flex items-center transition-colors"
            aria-label="Fechar painel de notificações"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        {/* Corpo com scroll */}
        <div className="p-4 overflow-y-auto flex-grow">
          <NotificacoesList
            notificacoes={notifications}
            onMarkAsRead={markAsRead}
            isAdminView={false}
          />
        </div>
      </div>
    </>
  );
}

export default NotificationPanel;
