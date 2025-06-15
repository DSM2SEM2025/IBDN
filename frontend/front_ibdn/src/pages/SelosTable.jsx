import React from "react";

// --- Ícones SVG ---
const ApproveIcon = (props) => (
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
      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
    ></path>
  </svg>
);

const RenewIcon = (props) => (
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
      d="M4 4v5h5M20 20v-5h-5M4 4l5 5M20 20l-5-5"
    ></path>
  </svg>
);

/**
 * Componente para exibir uma tabela de selos.
 * @param {Object} props
 * @param {Array} props.selos - A lista de selos a ser exibida (já formatada).
 * @param {Function} props.onApprove - Função para aprovar um selo.
 * @param {Function} props.onRenew - Função para solicitar renovação de um selo.
 */
function SelosTable({ selos, onApprove, onRenew }) {
  if (!selos || selos.length === 0) {
    return (
      <div className="text-center p-10 bg-white rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-700">
          Nenhum selo encontrado
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          Nenhum selo foi associado a uma empresa ainda.
        </p>
      </div>
    );
  }

  const getStatusClass = (status) => {
    switch (status) {
      case "ativo":
        return "bg-green-100 text-green-800";
      case "pendente":
        return "bg-yellow-100 text-yellow-800";
      case "expirado":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="overflow-x-auto bg-white rounded-lg shadow">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Empresa
            </th>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Código do Selo
            </th>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Status
            </th>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Validade
            </th>
            <th scope="col" className="relative px-6 py-3">
              <span className="sr-only">Ações</span>
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {selos.map((selo) => (
            <tr key={selo.id} className="hover:bg-gray-50 transition-colors">
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm font-medium text-gray-900">
                  {selo.empresa.razao_social}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm text-gray-500 font-mono">
                  {selo.codigo}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span
                  className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusClass(
                    selo.status
                  )}`}
                >
                  {selo.status}
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm text-gray-900">
                  Expira em: {selo.data_validade}
                </div>
                <div className="text-sm text-gray-500">
                  Emitido em: {selo.data_emissao}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div className="flex items-center justify-end space-x-4">
                  {selo.status === "pendente" && (
                    <button
                      onClick={() => onApprove(selo.id)}
                      className="text-green-600 hover:text-green-900"
                      title="Aprovar Selo"
                    >
                      <ApproveIcon className="w-5 h-5" />
                    </button>
                  )}
                  {selo.status === "expirado" && (
                    <button
                      onClick={() => onRenew(selo.id)}
                      className="text-blue-600 hover:text-blue-900"
                      title="Solicitar Renovação"
                    >
                      <RenewIcon className="w-5 h-5" />
                    </button>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default SelosTable;
