import React, { useState } from "react";

/**
 * Formulário para associar um novo selo a uma empresa.
 * @param {Object} props
 * @param {Function} props.onSubmit - Função chamada ao submeter o formulário.
 * @param {Function} props.onCancel - Função para cancelar e fechar.
 * @param {boolean} props.isSaving - Indica se o processo de salvar está em andamento.
 */
function AssociarSeloForm({ onSubmit, onCancel, isSaving }) {
  const [formData, setFormData] = useState({
    id_tipo_selo: "",
    dias_validade: 365,
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
    onSubmit({
      ...formData,
      id_tipo_selo: parseInt(formData.id_tipo_selo, 10), // Garante que o ID é um número
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Campo Tipo de Selo */}
      <div>
        <label
          htmlFor="id_tipo_selo"
          className="block text-sm font-medium text-gray-700"
        >
          ID do Tipo de Selo
        </label>
        <input
          type="number"
          name="id_tipo_selo"
          id="id_tipo_selo"
          value={formData.id_tipo_selo}
          onChange={handleChange}
          required
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          placeholder="Insira o ID do tipo de selo"
        />
        {/* Nota: Em um cenário real, isto seria idealmente um menu dropdown (select) */}
      </div>

      {/* Campo Dias de Validade */}
      <div>
        <label
          htmlFor="dias_validade"
          className="block text-sm font-medium text-gray-700"
        >
          Dias de Validade
        </label>
        <input
          type="number"
          name="dias_validade"
          id="dias_validade"
          value={formData.dias_validade}
          onChange={handleChange}
          required
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
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
          {isSaving ? "Associando..." : "Associar Selo"}
        </button>
      </div>
    </form>
  );
}

export default AssociarSeloForm;
