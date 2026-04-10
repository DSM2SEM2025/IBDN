import React from "react";
import { CheckCircle, XCircle, Inbox } from "lucide-react";

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
      <div className="text-center p-14 premium-card bg-white rounded-3xl shadow-sm border border-gray-100 flex flex-col items-center">
        <div className="w-16 h-16 rounded-full bg-ibdn-bg flex items-center justify-center mb-4">
          <Inbox className="w-8 h-8 text-ibdn-primary opacity-50" />
        </div>
        <h3 className="text-xl font-serif font-bold text-gray-800">
          Nenhuma solicitação pendente
        </h3>
        <p className="mt-2 text-md text-gray-500 max-w-sm">
          A caixa de entrada de novos selos e renovações está limpa no momento.
        </p>
      </div>
    );
  }

  return (
    <>
      <div className="md:hidden space-y-4">
        {solicitacoes.map((solicitacao) => (
          <div key={solicitacao.id} className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 flex flex-col gap-3 relative">
            <div className="flex justify-between items-start">
              <div className="text-base font-bold text-gray-900">{solicitacao.razao_social_empresa}</div>
              <span className="px-2 py-1 inline-flex text-xs font-bold rounded-full bg-yellow-100 text-yellow-800 border border-yellow-200 capitalize">
                {solicitacao.status}
              </span>
            </div>
            <div className="text-sm text-gray-600 font-mono bg-gray-50 px-2 py-1 rounded inline-block w-fit">
              {solicitacao.nome_selo} ({solicitacao.sigla_selo})
            </div>
            
            <div className="flex items-center justify-between space-x-2 mt-2 pt-3 border-t border-gray-50">
              <button 
                onClick={() => onReject(solicitacao.id)} 
                className="p-2 text-red-600 bg-red-50 hover:bg-red-100 rounded-lg flex items-center justify-center flex-1 font-medium text-sm transition-colors"
              >
                <XCircle className="w-4 h-4 mr-1.5" /> Recusar
              </button>
              <button 
                onClick={() => onApprove(solicitacao.id)} 
                className="p-2 text-green-600 bg-green-50 hover:bg-green-100 rounded-lg flex items-center justify-center flex-1 font-medium text-sm transition-colors"
              >
                <CheckCircle className="w-4 h-4 mr-1.5" /> Aprovar
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="hidden md:block overflow-x-auto premium-card bg-white rounded-3xl shadow-sm border border-gray-100">
      <table className="min-w-full divide-y divide-gray-100">
        <thead className="bg-ibdn-bg/50">
          <tr>
            <th
              scope="col"
              className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest rounded-tl-3xl font-serif"
            >
              Empresa
            </th>
            <th
              scope="col"
              className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest font-serif"
            >
              Tipo de Selo
            </th>
            <th
              scope="col"
              className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest font-serif"
            >
              Status
            </th>
            <th scope="col" className="relative px-6 py-4 rounded-tr-3xl">
              <span className="sr-only">Ações</span>
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-50">
          {solicitacoes.map((solicitacao) => (
            <tr key={solicitacao.id} className="hover:bg-ibdn-bg/30 transition-colors group">
              <td className="px-6 py-5 whitespace-nowrap">
                <div className="text-sm font-bold text-gray-900 group-hover:text-ibdn-primary transition-colors">
                  {solicitacao.razao_social_empresa}
                </div>
              </td>
              <td className="px-6 py-5 whitespace-nowrap">
                <div className="text-sm text-gray-600 font-mono bg-gray-50 px-2 py-1 rounded inline-block">
                  {solicitacao.nome_selo} ({solicitacao.sigla_selo})
                </div>
              </td>
              <td className="px-6 py-5 whitespace-nowrap">
                <span className="px-3 py-1 inline-flex text-xs leading-5 font-bold rounded-full bg-yellow-100 text-yellow-800 border border-yellow-200 capitalize">
                  {solicitacao.status}
                </span>
              </td>
              <td className="px-6 py-5 whitespace-nowrap text-right text-sm font-medium">
                <div className="flex items-center justify-end space-x-3 opacity-70 group-hover:opacity-100 transition-opacity">
                  <button
                    onClick={() => onApprove(solicitacao.id)}
                    className="p-2 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                    title="Aprovar Selo"
                  >
                    <CheckCircle className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => onReject(solicitacao.id)}
                    className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Recusar Selo"
                  >
                    <XCircle className="w-5 h-5" />
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>
    </>
  );
}

export default SolicitacoesSeloTable;
