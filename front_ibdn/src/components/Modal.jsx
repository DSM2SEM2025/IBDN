import React from "react";
import { X } from "lucide-react";

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
      className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex justify-center items-center p-4 transition-all"
      onClick={onClose} // Fecha o modal ao clicar fora dele.
    >
      {/* Conteúdo do Modal */}
      <div
        className="bg-white rounded-3xl shadow-2xl border border-gray-100 w-full max-w-2xl max-h-[90vh] flex flex-col transform transition-all overflow-hidden"
        onClick={(e) => e.stopPropagation()} // Impede que o clique dentro do modal o feche.
      >
        {/* Cabeçalho do Modal */}
        <div className="flex justify-between items-center px-6 py-5 border-b border-gray-100 bg-ibdn-bg/30">
          <h3 className="text-xl font-bold font-serif text-ibdn-earthy">{title}</h3>
          <button
            onClick={onClose}
            className="text-gray-400 bg-transparent hover:bg-gray-100 hover:text-red-500 rounded-full p-2 ml-auto inline-flex items-center transition-colors"
            aria-label="Fechar modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        {/* Corpo do Modal (com scroll se o conteúdo for grande) */}
        <div className="p-6 overflow-y-auto">{children}</div>
      </div>
    </div>
  );
}

export default Modal;
