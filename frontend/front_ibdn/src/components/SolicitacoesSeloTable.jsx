import React from "react";

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

// --- NOVO ÍCONE DE RECUSAR ---
const RejectIcon = (props) => (
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
      d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
    ></path>
  </svg>
);

const formatDate = (dateString) => {
  if (!dateString) return "Pendente de Data";
  try {
    const date = new Date(dateString);
    const userTimezoneOffset = date.getTimezoneOffset() * 60000;
    return new Date(date.getTime() + userTimezoneOffset).toLocaleDateString(
      "pt-BR"
    );
  } catch (error) {
    return "Data Inválida";
  }
};

function SolicitacoesSeloTable({ solicitacoes, onApprove, onReject }) {
  if (!solicitacoes || solicitacoes.length === 0) {
    return (
      <div className="text-center p-10 bg-white rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-700">
          Nenhuma solicitação pendente
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          Não há selos aguardando aprovação no momento.
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
              Tipo de Selo
            </th>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Status
            </th>
            <th scope="col" className="relative px-6 py-3">
              <span className="sr-only">Ações</span>
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {solicitacoes.map((solicitacao) => (
            <tr key={solicitacao.id} className="hover:bg-gray-50">
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {solicitacao.razao_social_empresa}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {solicitacao.nome_selo} ({solicitacao.sigla_selo})
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 capitalize">
                {solicitacao.status}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div className="flex items-center justify-end space-x-4">
                  <button
                    onClick={() => onApprove(solicitacao.id)}
                    className="text-green-600 hover:text-green-900"
                    title="Aprovar Selo"
                  >
                    <ApproveIcon className="w-6 h-6" />
                  </button>
                  {/* --- NOVO BOTÃO DE RECUSAR --- */}
                  <button
                    onClick={() => onReject(solicitacao.id)}
                    className="text-red-600 hover:text-red-900"
                    title="Recusar Selo"
                  >
                    <RejectIcon className="w-6 h-6" />
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

export default SolicitacoesSeloTable;
