import React from "react";
import useNotificationStore from "../store/notificationStore";

const BellIcon = (props) => (
  <svg
    {...props}
    fill="none"
    stroke="currentColor"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth="2"
      d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 10-12 0v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
    ></path>
  </svg>
);

function NotificationIcon() {
  const { unreadCount, togglePanel } = useNotificationStore();

  return (
    <button
      onClick={togglePanel}
      className="fixed bottom-6 right-6 bg-green-900 text-white w-16 h-16 rounded-full shadow-lg flex items-center justify-center hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 z-50"
      aria-label="Abrir notificações"
    >
      <BellIcon className="w-8 h-8" />
      {unreadCount > 0 && (
        <span className="absolute top-0 right-0 block h-6 w-6 transform -translate-y-1/4 translate-x-1/4 rounded-full bg-red-600 text-white text-xs flex items-center justify-center ring-2 ring-white">
          {unreadCount}
        </span>
      )}
    </button>
  );
}

export default NotificationIcon;
