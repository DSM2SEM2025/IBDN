import React, { useState, useEffect } from "react";

function SolicitarSeloForm({ tiposSelo = [], onSubmit, onCancel, isSaving }) {
  const [formData, setFormData] = useState({
    id_selo: "",
    plano_anos: 1, // Valor inicial para o plano
  });

  useEffect(() => {
    if (tiposSelo.length > 0) {
      setFormData((prev) => ({ ...prev, id_selo: tiposSelo[0].id.toString() }));
    }
  }, [tiposSelo]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.id_selo) {
      // Envia o objeto formData completo, com os tipos corretos
      onSubmit({
        id_selo: parseInt(formData.id_selo, 10),
        plano_anos: parseInt(formData.plano_anos, 10),
      });
    } else {
      alert("Por favor, selecione um tipo de selo.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label
          htmlFor="id_selo"
          className="block text-sm font-medium text-gray-700"
        >
          Selecione o Tipo de Selo
        </label>
        <select
          id="id_selo"
          name="id_selo"
          value={formData.id_selo}
          onChange={handleChange}
          required
          className="mt-1 block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
        >
          {tiposSelo.length === 0 && (
            <option value="">Nenhum selo disponível</option>
          )}
          {tiposSelo.map((selo) => (
            <option key={selo.id} value={selo.id}>
              {selo.nome} ({selo.sigla})
            </option>
          ))}
        </select>
      </div>

      {/* NOVO CAMPO PARA O PLANO */}
      <div>
        <label
          htmlFor="plano_anos"
          className="block text-sm font-medium text-gray-700"
        >
          Selecione o Plano de Validade
        </label>
        <select
          id="plano_anos"
          name="plano_anos"
          value={formData.plano_anos}
          onChange={handleChange}
          required
          className="mt-1 block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
        >
          <option value="1">1 Ano</option>
          <option value="2">2 Anos</option>
          <option value="3">3 Anos</option>
        </select>
      </div>

      <div className="flex justify-end space-x-4 pt-4">
        <button
          type="button"
          onClick={onCancel}
          disabled={isSaving}
          className="rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 disabled:opacity-50"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={isSaving || tiposSelo.length === 0}
          className="inline-flex justify-center rounded-md border border-transparent bg-green-900 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-green-700 disabled:opacity-50"
        >
          {isSaving ? "Enviando..." : "Solicitar Selo"}
        </button>
      </div>
    </form>
  );
}

export default SolicitarSeloForm;
