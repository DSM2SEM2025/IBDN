import React from "react";

// --- Ícones SVG ---
const EditIcon = (props) => (
  <svg
    {...props}
    fill="none"
    stroke="currentColor"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.5L14.732 3.732z"
    />
  </svg>
);

const DeleteIcon = (props) => (
  <svg
    {...props}
    fill="none"
    stroke="currentColor"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-4v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
    />
  </svg>
);

const ManageIcon = (props) => (
  <svg
    {...props}
    fill="none"
    stroke="currentColor"
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth="2"
      d="M12 6V4m0 16v-2m0-8v-2m0 4h.01M6 12H4m16 0h-2m-8-2h.01M12 18h.01M8 8h.01M16 16h.01M16 8h.01M8 16h.01"
    ></path>
  </svg>
);

/**
 * Componente para exibir uma tabela de perfis de utilizador.
 * @param {Object} props
 * @param {Array} props.perfis - A lista de perfis a ser exibida.
 * @param {Function} props.onEdit - Função para editar o nome do perfil.
 * @param {Function} props.onDelete - Função para excluir o perfil.
 * @param {Function} props.onManagePermissions - Função para gerir as permissões do perfil.
 */
function PerfisTable({ perfis, onEdit, onDelete, onManagePermissions }) {
  if (!perfis || perfis.length === 0) {
    return (
      <div className="text-center p-10 bg-white rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-700">
          Nenhum perfil encontrado
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          Pode começar por adicionar um novo perfil.
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto bg-white rounded-lg shadow">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Nome do Perfil
            </th>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Permissões
            </th>
            <th scope="col" className="relative px-6 py-3">
              <span className="sr-only">Ações</span>
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {perfis.map((perfil) => (
            <tr key={perfil.id} className="hover:bg-gray-50 transition-colors">
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm font-medium text-gray-900">
                  {perfil.nome}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm text-gray-500">
                  {perfil.permissoes?.length || 0}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div className="flex items-center justify-end space-x-4">
                  <button
                    onClick={() => onManagePermissions(perfil)}
                    className="text-gray-500 hover:text-indigo-600"
                    title="Gerir Permissões"
                  >
                    <ManageIcon className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => onEdit(perfil)}
                    className="text-indigo-600 hover:text-indigo-900"
                    title="Editar"
                  >
                    <EditIcon className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => onDelete(perfil.id)}
                    className="text-red-600 hover:text-red-900"
                    title="Excluir"
                  >
                    <DeleteIcon className="w-5 h-5" />
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default PerfisTable;
