import React from "react";

/**
 * Componente de modal genérico e reutilizável.
 * @param {Object} props
 * @param {boolean} props.isOpen - Controla a visibilidade do modal.
 * @param {Function} props.onClose - Função para fechar o modal.
 * @param {string} props.title - O título a ser exibido no cabeçalho do modal.
 * @param {React.ReactNode} props.children - O conteúdo a ser renderizado dentro do modal.
 */
function Modal({ isOpen, onClose, title, children }) {
  // Se não estiver aberto, não renderiza nada.
  if (!isOpen) return null;

  return (
    // Backdrop: um fundo semi-transparente que cobre a página.
    <div
      className="fixed inset-0 bg-black bg-opacity-50 z-40 flex justify-center items-start pt-16 px-4"
      onClick={onClose} // Fecha o modal ao clicar fora dele.
    >
      {/* Conteúdo do Modal */}
      <div
        className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] flex flex-col"
        onClick={(e) => e.stopPropagation()} // Impede que o clique dentro do modal o feche.
      >
        {/* Cabeçalho do Modal */}
        <div className="flex justify-between items-center p-4 border-b">
          <h3 className="text-xl font-semibold text-gray-900">{title}</h3>
          <button
            onClick={onClose}
            className="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center"
            aria-label="Fechar modal"
          >
            {/* Ícone 'X' para fechar */}
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clipRule="evenodd"
              ></path>
            </svg>
          </button>
        </div>
        {/* Corpo do Modal (com scroll se o conteúdo for grande) */}
        <div className="p-6 overflow-y-auto">{children}</div>
      </div>
    </div>
  );
}

export default Modal;
