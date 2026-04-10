import React from "react";
import { CheckCircle, RotateCw, FileBadge2 } from "lucide-react";

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
      <div className="text-center p-14 premium-card bg-white rounded-3xl shadow-sm border border-gray-100 flex flex-col items-center">
        <div className="w-16 h-16 rounded-full bg-ibdn-bg flex items-center justify-center mb-4">
          <FileBadge2 className="w-8 h-8 text-ibdn-primary opacity-50" />
        </div>
        <h3 className="text-xl font-serif font-bold text-gray-800">
          Nenhum selo ativo
        </h3>
        <p className="mt-2 text-md text-gray-500 max-w-sm">
          A lista de selos está vazia. Comece associando um selo a uma entidade na tela de Cadastro.
        </p>
      </div>
    );
  }

  return (
    <>
      <div className="md:hidden space-y-4">
        {selos.map((selo) => (
          <div key={selo.id} className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 flex flex-col gap-3 relative">
            <div className="flex justify-between items-start">
              <div className="flex flex-col">
                <div className="text-base font-bold text-gray-900">{selo.empresa?.razao_social || "N/A"}</div>
                <div className="text-xs text-gray-500 font-mono bg-gray-50 px-2 py-1 rounded inline-block mt-1 w-fit">
                  {selo.sigla_selo || selo.codigo}
                </div>
              </div>
              <span className={`px-2 py-1 inline-flex text-xs font-bold rounded-full border ${selo.status === "ativo" ? "bg-green-100 text-green-800 border-green-200" : "bg-yellow-100 text-yellow-800 border-yellow-200"}`}>
                {selo.status}
              </span>
            </div>
            <div className="flex justify-between mt-1 text-sm">
              <div className="text-gray-900 font-medium">Validade: {formatDate(selo.data_validade)}</div>
              <div className="text-gray-500">Emitido: {formatDate(selo.data_emissao)}</div>
            </div>
            
            <div className="flex items-center justify-end space-x-2 mt-2 pt-3 border-t border-gray-50">
              {selo.status !== "ativo" && (
                <button onClick={() => onApprove(selo.id)} className="p-2 text-green-600 bg-green-50 rounded-lg flex items-center justify-center flex-1 font-medium text-sm">
                  <CheckCircle className="w-4 h-4 mr-1.5" /> Aprovar
                </button>
              )}
              <button 
                onClick={() => onRenew(selo.id)} 
                className={`p-2 text-blue-600 bg-blue-50 rounded-lg flex items-center justify-center font-medium text-sm ${selo.status === 'ativo' ? 'flex-1' : ''}`}
              >
                <RotateCw className="w-4 h-4 mr-1.5" /> Renovação
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
              Código do Selo
            </th>
            <th
              scope="col"
              className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest font-serif"
            >
              Status
            </th>
            <th
              scope="col"
              className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest font-serif"
            >
              Validade
            </th>
            <th scope="col" className="relative px-6 py-4 rounded-tr-3xl">
              <span className="sr-only">Ações</span>
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-50">
          {selos.map((selo) => (
            <tr key={selo.id} className="hover:bg-ibdn-bg/30 transition-colors group">
              <td className="px-6 py-5 whitespace-nowrap">
                <div className="text-sm font-bold text-gray-900 group-hover:text-ibdn-primary transition-colors">
                  {selo.empresa?.razao_social || "N/A"}
                </div>
              </td>
              <td className="px-6 py-5 whitespace-nowrap">
                <div className="text-sm text-gray-600 font-mono bg-gray-50 px-2 py-1 rounded inline-block">
                  {selo.sigla_selo || selo.codigo}
                </div>
              </td>
              <td className="px-6 py-5 whitespace-nowrap">
                <span
                  className={`px-3 py-1 inline-flex text-xs leading-5 font-bold rounded-full border ${
                    selo.status === "ativo"
                      ? "bg-green-100 text-green-800 border-green-200"
                      : "bg-yellow-100 text-yellow-800 border-yellow-200"
                  }`}
                >
                  {selo.status}
                </span>
              </td>
              <td className="px-6 py-5 whitespace-nowrap">
                <div className="text-sm text-gray-900 font-medium">
                  {formatDate(selo.data_validade)}
                </div>
                <div className="text-xs text-gray-500 mt-0.5">
                  Emitido em: {formatDate(selo.data_emissao)}
                </div>
              </td>
              <td className="px-6 py-5 whitespace-nowrap text-right text-sm font-medium">
                <div className="flex items-center justify-end space-x-3 opacity-70 group-hover:opacity-100 transition-opacity">
                  {selo.status !== "ativo" && (
                    <button
                      onClick={() => onApprove(selo.id)}
                      className="p-2 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                      title="Aprovar Selo"
                    >
                      <CheckCircle className="w-5 h-5" />
                    </button>
                  )}
                  <button
                    onClick={() => onRenew(selo.id)}
                    className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                    title="Solicitar Renovação"
                  >
                    <RotateCw className="w-5 h-5" />
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

export default SelosTable;
