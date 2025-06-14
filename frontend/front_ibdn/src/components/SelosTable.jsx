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
    touch
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
 * Formata uma data string (YYYY-MM-DD) para o formato local (DD/MM/YYYY).
 * @param {string} dateString - A data em formato string.
 * @returns {string} A data formatada.
 */
const formatDate = (dateString) => {
  if (!dateString) return "-";
  try {
    const date = new Date(dateString);
    // Adiciona o fuso horário para corrigir a exibição da data
    const userTimezoneOffset = date.getTimezoneOffset() * 60000;
    return new Date(date.getTime() + userTimezoneOffset).toLocaleDateString(
      "pt-BR"
    );
  } catch (error) {
    return "Data inválida";
  }
};

/**
 * Componente para exibir uma tabela de selos.
 * @param {Object} props
 * @param {Array} props.selos - A lista de selos a ser exibida.
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
          Pode começar por associar um selo a uma empresa.
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
                  {selo.empresa?.razao_social || "N/A"}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm text-gray-500 font-mono">
                  {selo.codigo}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span
                  className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    selo.status === "ativo"
                      ? "bg-green-100 text-green-800"
                      : "bg-yellow-100 text-yellow-800"
                  }`}
                >
                  {selo.status}
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm text-gray-900">
                  {formatDate(selo.data_validade)}
                </div>
                <div className="text-sm text-gray-500">
                  Emitido em: {formatDate(selo.data_emissao)}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div className="flex items-center justify-end space-x-4">
                  {selo.status !== "ativo" && (
                    <button
                      onClick={() => onApprove(selo.id)}
                      className="text-green-600 hover:text-green-900"
                      title="Aprovar Selo"
                    >
                      <ApproveIcon className="w-5 h-5" />
                    </button>
                  )}
                  <button
                    onClick={() => onRenew(selo.id)}
                    className="text-blue-600 hover:text-blue-900"
                    title="Solicitar Renovação"
                  >
                    <RenewIcon className="w-5 h-5" />
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

export default SelosTable;
