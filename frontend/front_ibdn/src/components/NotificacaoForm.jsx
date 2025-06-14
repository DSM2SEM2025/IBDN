import React, { useState } from "react";

/**
 * Formulário para criar uma nova notificação para uma empresa.
 * @param {Object} props
 * @param {Function} props.onSubmit - Função chamada ao submeter o formulário.
 * @param {Function} props.onCancel - Função para cancelar e fechar.
 * @param {boolean} props.isSaving - Indica se o processo de salvar está em andamento.
 */
function NotificacaoForm({ onSubmit, onCancel, isSaving }) {
  const [formData, setFormData] = useState({
    mensagem: "",
    tipo: "info", // Valor padrão para o tipo
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Campo Mensagem */}
      <div>
        <label
          htmlFor="mensagem"
          className="block text-sm font-medium text-gray-700"
        >
          Mensagem
        </label>
        <textarea
          name="mensagem"
          id="mensagem"
          value={formData.mensagem}
          onChange={handleChange}
          required
          rows={4}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          placeholder="Escreva a mensagem da notificação aqui..."
        />
      </div>

      {/* Campo Tipo */}
      <div>
        <label
          htmlFor="tipo"
          className="block text-sm font-medium text-gray-700"
        >
          Tipo de Notificação
        </label>
        <select
          id="tipo"
          name="tipo"
          value={formData.tipo}
          onChange={handleChange}
          className="mt-1 block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
        >
          <option value="info">Info</option>
          <option value="aviso">Aviso</option>
          <option value="erro">Erro</option>
        </select>
      </div>

      {/* Botões de Ação */}
      <div className="flex justify-end space-x-4 pt-4">
        <button
          type="button"
          onClick={onCancel}
          disabled={isSaving}
          className="rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={isSaving}
          className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {isSaving ? "Enviando..." : "Enviar Notificação"}
        </button>
      </div>
    </form>
  );
}

export default NotificacaoForm;
