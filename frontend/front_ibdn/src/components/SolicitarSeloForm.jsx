// front_e_back/front/src/components/SolicitarSeloForm.jsx
import React, { useState, useEffect } from "react";

function SolicitarSeloForm({ tiposSelo = [], onSubmit, onCancel, isSaving }) {
  const [selectedSeloId, setSelectedSeloId] = useState("");

  useEffect(() => {
    if (tiposSelo.length > 0) {
      setSelectedSeloId(tiposSelo[0].id.toString());
    }
  }, [tiposSelo]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedSeloId) {
      onSubmit(parseInt(selectedSeloId, 10));
    } else {
      alert("Por favor, selecione um tipo de selo.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label
          htmlFor="tipo_selo"
          className="block text-sm font-medium text-gray-700"
        >
          Selecione o Tipo de Selo
        </label>
        <select
          id="tipo_selo"
          name="tipo_selo"
          value={selectedSeloId}
          onChange={(e) => setSelectedSeloId(e.target.value)}
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
          className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 disabled:opacity-50"
        >
          {isSaving ? "Enviando..." : "Solicitar Selo"}
        </button>
      </div>
    </form>
  );
}

export default SolicitarSeloForm;
