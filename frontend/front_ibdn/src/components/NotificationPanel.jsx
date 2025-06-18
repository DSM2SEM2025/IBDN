import React from "react";
import useNotificationStore from "../store/notificationStore";
import NotificacoesList from "./NotificacoesList";

function NotificationPanel() {
  const { isPanelOpen, notifications, markAsRead, closePanel } =
    useNotificationStore();

  if (!isPanelOpen) return null;

  return (
    <>
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40"
        onClick={closePanel}
      ></div>
      {/* Painel */}
      <div className="fixed top-0 right-0 h-full w-full max-w-sm bg-white shadow-lg z-50 transform transition-transform translate-x-0">
        <div className="flex flex-col h-full">
          <div className="flex justify-between items-center p-4 border-b">
            <h3 className="text-xl font-semibold text-gray-900">
              Notificações
            </h3>
            <button
              onClick={closePanel}
              className="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clipRule="evenodd"
                ></path>
              </svg>
            </button>
          </div>
          <div className="p-4 overflow-y-auto flex-grow">
            <NotificacoesList
              notificacoes={notifications}
              onMarkAsRead={markAsRead}
              isAdminView={false} // A visão do painel é sempre a do usuário da empresa
            />
          </div>
        </div>
      </div>
    </>
  );
}

export default NotificationPanel;
