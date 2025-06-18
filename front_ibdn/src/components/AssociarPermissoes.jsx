import React, { useState, useEffect } from "react";

/**
 * Componente para associar ou desassociar permissões a um perfil.
 * @param {Object} props
 * @param {Object} props.perfil - O perfil que está a ser editado.
 * @param {Array} props.todasPermissoes - A lista de todas as permissões disponíveis no sistema.
 * @param {Function} props.onSave - Função chamada ao salvar, passando os IDs das permissões selecionadas.
 * @param {Function} props.onCancel - Função para cancelar e fechar.
 * @param {boolean} props.isSaving - Indica se o processo de salvar está em andamento.
 */
function AssociarPermissoes({
  perfil,
  todasPermissoes,
  onSave,
  onCancel,
  isSaving,
}) {
  const [selectedPermissoes, setSelectedPermissoes] = useState(new Set());

  // Efeito para inicializar as permissões selecionadas com base no perfil atual
  useEffect(() => {
    if (perfil && perfil.permissoes) {
      const idsDasPermissoesAtuais = new Set(
        perfil.permissoes.map((p) => p.id)
      );
      setSelectedPermissoes(idsDasPermissoesAtuais);
    }
  }, [perfil]);

  // Função para lidar com a mudança de uma checkbox
  const handleCheckboxChange = (permissaoId) => {
    setSelectedPermissoes((prevSelected) => {
      const newSelected = new Set(prevSelected);
      if (newSelected.has(permissaoId)) {
        newSelected.delete(permissaoId);
      } else {
        newSelected.add(permissaoId);
      }
      return newSelected;
    });
  };

  const handleSave = () => {
    // Converte o Set de volta para um array de IDs antes de salvar
    onSave(Array.from(selectedPermissoes));
  };

  return (
    <div>
      <h4 className="text-lg font-medium text-gray-800 mb-4">
        Gerir permissões para o perfil:{" "}
        <span className="font-bold">{perfil?.nome}</span>
      </h4>

      {/* Lista de Permissões com Checkboxes */}
      <div className="space-y-4 max-h-96 overflow-y-auto border p-4 rounded-md">
        {todasPermissoes.length > 0 ? (
          todasPermissoes.map((permissao) => (
            <div key={permissao.id} className="flex items-center">
              <input
                id={`permissao-${permissao.id}`}
                name={permissao.nome}
                type="checkbox"
                checked={selectedPermissoes.has(permissao.id)}
                onChange={() => handleCheckboxChange(permissao.id)}
                className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              />
              <label
                htmlFor={`permissao-${permissao.id}`}
                className="ml-3 block text-sm font-medium text-gray-700"
              >
                {permissao.nome}
              </label>
            </div>
          ))
        ) : (
          <p className="text-sm text-gray-500">
            Nenhuma permissão disponível no sistema.
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
          className="inline-flex justify-center rounded-md border border-transparent bg-green-900 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {isSaving ? "Salvando..." : "Salvar Permissões"}
        </button>
      </div>
    </div>
  );
}

export default AssociarPermissoes;
