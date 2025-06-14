import React, { useState, useEffect } from "react";

/**
 * Componente para associar ou desassociar ramos a uma empresa.
 * @param {Object} props
 * @param {Array} props.ramosAtuais - Os ramos atualmente associados à empresa.
 * @param {Array} props.todosOsRamos - A lista de todos os ramos disponíveis no sistema.
 * @param {Function} props.onSave - Função chamada ao salvar, passando os IDs dos ramos selecionados.
 * @param {Function} props.onCancel - Função para cancelar e fechar.
 * @param {boolean} props.isSaving - Indica se o processo de salvar está em andamento.
 */
function AssociarRamosForm({
  ramosAtuais = [],
  todosOsRamos = [],
  onSave,
  onCancel,
  isSaving,
}) {
  const [selectedRamos, setSelectedRamos] = useState(new Set());

  // Efeito para inicializar os ramos selecionados com base nos dados atuais
  useEffect(() => {
    const idsDosRamosAtuais = new Set(ramosAtuais.map((r) => r.id));
    setSelectedRamos(idsDosRamosAtuais);
  }, [ramosAtuais]);

  // Função para lidar com a mudança de uma checkbox
  const handleCheckboxChange = (ramoId) => {
    setSelectedRamos((prevSelected) => {
      const newSelected = new Set(prevSelected);
      if (newSelected.has(ramoId)) {
        newSelected.delete(ramoId);
      } else {
        newSelected.add(ramoId);
      }
      return newSelected;
    });
  };

  const handleSave = () => {
    // Converte o Set de volta para um array de IDs antes de salvar
    onSave(Array.from(selectedRamos));
  };

  return (
    <div>
      <h4 className="text-lg font-medium text-gray-800 mb-4">
        Selecione os ramos de atividade
      </h4>

      {/* Lista de Ramos com Checkboxes */}
      <div className="space-y-4 max-h-96 overflow-y-auto border p-4 rounded-md">
        {todosOsRamos.length > 0 ? (
          todosOsRamos.map((ramo) => (
            <div key={ramo.id} className="flex items-center">
              <input
                id={`ramo-${ramo.id}`}
                name={ramo.nome}
                type="checkbox"
                checked={selectedRamos.has(ramo.id)}
                onChange={() => handleCheckboxChange(ramo.id)}
                className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              />
              <label
                htmlFor={`ramo-${ramo.id}`}
                className="ml-3 block text-sm font-medium text-gray-700"
              >
                {ramo.nome}
              </label>
            </div>
          ))
        ) : (
          <p className="text-sm text-gray-500">
            Nenhum ramo de atividade disponível no sistema.
          </p>
        )}
      </div>

      {/* Botões de Ação */}
      <div className="flex justify-end space-x-4 pt-6">
        <button
          type="button"
          onClick={onCancel}
          disabled={isSaving}
          className="rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
        >
          Cancelar
        </button>
        <button
          type="button"
          onClick={handleSave}
          disabled={isSaving}
          className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {isSaving ? "Salvando..." : "Salvar Ramos"}
        </button>
      </div>
    </div>
  );
}

export default AssociarRamosForm;
