import React from "react";

// Ícones SVG para as ações
const CheckIcon = (props) => (
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
      strokeWidth={2}
      d="M5 13l4 4L19 7"
    />
  </svg>
);

const DeleteIcon = (props) => (
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
      strokeWidth={2}
      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-4v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
    />
  </svg>
);

// Helper para formatar a data para um formato mais legível
const formatDate = (dateString) => {
  if (!dateString) return "-";
  try {
    const date = new Date(dateString);
    return date.toLocaleString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch (error) {
    return "Data inválida";
  }
};

/**
 * Componente para exibir uma lista de notificações.
 * @param {Object} props
 * @param {Array} props.notificacoes - A lista de notificações a ser exibida.
 * @param {Function} props.onMarkAsRead - Função para marcar uma notificação como lida.
 * @param {Function} props.onDelete - Função para excluir uma notificação.
 */
function NotificacoesList({ notificacoes, onMarkAsRead, onDelete }) {
  if (!notificacoes || notificacoes.length === 0) {
    return (
      <div className="text-center p-6 bg-gray-50 rounded-lg">
        <h3 className="text-md font-semibold text-gray-600">
          Nenhuma notificação encontrada
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          Esta empresa não tem notificações.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {notificacoes.map((notificacao) => (
        <div
          key={notificacao.id}
          className={`p-4 rounded-lg shadow-sm flex items-start justify-between transition-colors ${
            notificacao.lida ? "bg-gray-100 text-gray-500" : "bg-white"
          }`}
        >
          <div className="flex-1">
            <div className="flex items-center mb-1">
              <span
                className={`px-2 py-0.5 text-xs font-semibold rounded-full mr-3 capitalize ${
                  notificacao.tipo === "info"
                    ? "bg-blue-100 text-blue-800"
                    : notificacao.tipo === "aviso"
                    ? "bg-yellow-100 text-yellow-800"
                    : "bg-red-100 text-red-800"
                }`}
              >
                {notificacao.tipo}
              </span>
              <span className="text-xs text-gray-400">
                {formatDate(notificacao.data_envio)}
              </span>
            </div>
            <p
              className={`text-sm ${
                notificacao.lida ? "text-gray-500" : "text-gray-800"
              }`}
            >
              {notificacao.mensagem}
            </p>
          </div>

          <div className="flex items-center space-x-3 ml-4">
            {!notificacao.lida && (
              <button
                onClick={() => onMarkAsRead(notificacao.id)}
                className="text-green-500 hover:text-green-700"
                title="Marcar como lida"
              >
                <CheckIcon className="w-5 h-5" />
              </button>
            )}
            <button
              onClick={() => onDelete(notificacao.id)}
              className="text-red-500 hover:text-red-700"
              title="Excluir notificação"
            >
              <DeleteIcon className="w-5 h-5" />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default NotificacoesList;
