// src/components/TipoSeloForm.jsx
import React, { useState, useEffect } from "react";

function TipoSeloForm({ initialData = {}, onSubmit, onCancel, isSaving }) {
  const [formData, setFormData] = useState({
    nome: "",
    descricao: "",
    sigla: "",
  });

  useEffect(() => {
    if (initialData.id) {
      setFormData({
        nome: initialData.nome || "",
        descricao: initialData.descricao || "",
        sigla: initialData.sigla || "",
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label
          htmlFor="nome"
          className="block text-sm font-medium text-gray-700"
        >
          Nome do Selo
        </label>
        <input
          type="text"
          name="nome"
          id="nome"
          value={formData.nome}
          onChange={handleChange}
          required
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
      </div>
      <div>
        <label
          htmlFor="sigla"
          className="block text-sm font-medium text-gray-700"
        >
          Sigla
        </label>
        <input
          type="text"
          name="sigla"
          id="sigla"
          value={formData.sigla}
          onChange={handleChange}
          required
          maxLength="10"
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
      </div>
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
          required
          rows={4}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
      </div>
      <div className="flex justify-end space-x-4 pt-4">
        <button
          type="button"
          onClick={onCancel}
          disabled={isSaving}
          className="rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={isSaving}
          className="inline-flex justify-center rounded-md border border-transparent bg-green-900 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-green-700"
        >
          {isSaving ? "Salvando..." : "Salvar"}
        </button>
      </div>
    </form>
  );
}

export default TipoSeloForm;
