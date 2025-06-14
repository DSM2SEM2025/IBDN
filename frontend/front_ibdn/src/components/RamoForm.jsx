import React, { useState, useEffect } from "react";

/**
 * Formulário para criar ou editar um ramo de atividade.
 * @param {Object} props
 * @param {Object} [props.initialData={}] - Os dados iniciais para preenchimento (para edição).
 * @param {Function} props.onSubmit - Função chamada ao submeter o formulário.
 * @param {Function} props.onCancel - Função para cancelar e fechar.
 * @param {boolean} props.isSaving - Indica se o processo de salvar está em andamento.
 */
function RamoForm({ initialData = {}, onSubmit, onCancel, isSaving }) {
  const [formData, setFormData] = useState({
    nome: "",
    descricao: "",
  });

  // Efeito para atualizar o formulário se os dados iniciais mudarem (modo de edição)
  useEffect(() => {
    if (initialData) {
      setFormData({
        nome: initialData.nome || "",
        descricao: initialData.descricao || "",
      });
    }
  }, [initialData]);

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
      {/* Campo Nome */}
      <div>
        <label
          htmlFor="nome"
          className="block text-sm font-medium text-gray-700"
        >
          Nome do Ramo
        </label>
        <input
          type="text"
          name="nome"
          id="nome"
          value={formData.nome}
          onChange={handleChange}
          required
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          placeholder="Ex: Tecnologia"
        />
      </div>

      {/* Campo Descrição */}
      <div>
        <label
          htmlFor="descricao"
          className="block text-sm font-medium text-gray-700"
        >
          Descrição
        </label>
        <textarea
          name="descricao"
          id="descricao"
          value={formData.descricao}
          onChange={handleChange}
          rows={3}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          placeholder="Descreva brevemente este ramo de atividade."
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
          {isSaving ? "Salvando..." : "Salvar"}
        </button>
      </div>
    </form>
  );
}

export default RamoForm;
