import React from "react";
import { Link } from "react-router-dom";
import { Pencil, Trash2, Award, Building2 } from "lucide-react";

/**
 * Componente para exibir uma tabela de empresas.
 * @param {Object} props
 * @param {Array} props.empresas - A lista de empresas a ser exibida.
 * @param {Function} props.onEdit - Função para editar a empresa.
 * @param {Function} props.onDelete - Função para excluir a empresa.
 * @param {Function} props.onAssociateSelo - Função para associar um selo à empresa.
 */
function EmpresasTable({ empresas, onEdit, onDelete, onAssociateSelo }) {
  if (!empresas || empresas.length === 0) {
    return (
      <div className="text-center p-14 premium-card bg-white rounded-3xl shadow-sm border border-gray-100 flex flex-col items-center">
        <div className="w-16 h-16 rounded-full bg-ibdn-bg flex items-center justify-center mb-4">
          <Building2 className="w-8 h-8 text-ibdn-primary opacity-50" />
        </div>
        <h3 className="text-xl font-serif font-bold text-gray-800">
          Nenhuma organização ativa
        </h3>
        <p className="mt-2 text-md text-gray-500 max-w-sm">
          A sua lista de empresas está vazia no momento. Adicione a sua primeira organização para iniciar os cadastros.
        </p>
      </div>
    );
  }

  return (
    <>
      {/* Visão Mobile (Cards) */}
      <div className="md:hidden space-y-4">
        {empresas.map((empresa) => (
          <div key={empresa.id} className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 flex flex-col gap-3 relative">
            <div className="flex justify-between items-start">
              <Link
                to={`/empresas/${empresa.id}`}
                className="flex flex-col"
              >
                <div className="text-base font-bold text-gray-900">{empresa.razao_social}</div>
                <div className="text-sm text-gray-500 mt-0.5">{empresa.nome_fantasia || "-"}</div>
              </Link>
              {empresa.ativo ? (
                <span className="px-2 py-1 inline-flex text-xs font-bold rounded-full bg-green-100 text-green-800 border border-green-200">
                  Ativo
                </span>
              ) : (
                <span className="px-2 py-1 inline-flex text-xs font-bold rounded-full bg-red-100 text-red-800 border border-red-200">
                  Inativo
                </span>
              )}
            </div>
            <div className="text-sm text-gray-600 font-mono bg-gray-50 px-2 py-1 rounded inline-block w-fit">
              {empresa.cnpj}
            </div>
            <div className="flex items-center justify-end space-x-2 mt-2 pt-3 border-t border-gray-50">
              <button
                onClick={() => onAssociateSelo(empresa.id)}
                className="p-2 text-ibdn-accent bg-ibdn-accent/5 hover:bg-ibdn-accent/10 rounded-lg transition-colors flex flex-1 items-center justify-center font-medium text-sm"
                title="Associar Selo"
              >
                <Award className="w-4 h-4 mr-1.5" /> Associar
              </button>
              <button
                onClick={() => onEdit(empresa.id)}
                className="p-2 text-gray-500 bg-gray-50 hover:text-ibdn-primary rounded-lg transition-colors"
                title="Editar"
              >
                <Pencil className="w-4 h-4" />
              </button>
              <button
                onClick={() => onDelete(empresa.id)}
                className="p-2 text-gray-500 bg-gray-50 hover:text-red-600 rounded-lg transition-colors"
                title="Excluir"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Visão Desktop (Tabela) */}
      <div className="hidden md:block overflow-x-auto premium-card bg-white rounded-3xl shadow-sm border border-gray-100">
      <table className="min-w-full divide-y divide-gray-100">
        <thead className="bg-ibdn-bg/50">
          <tr>
            <th
              scope="col"
              className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest rounded-tl-3xl font-serif"
            >
              Razão Social
            </th>
            <th
              scope="col"
              className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest font-serif"
            >
              CNPJ
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
          {empresas.map((empresa) => (
            <tr key={empresa.id} className="hover:bg-ibdn-bg/30 transition-colors group">
              <td className="px-6 py-5 whitespace-nowrap">
                <Link
                  to={`/empresas/${empresa.id}`}
                  className="flex flex-col group-hover:-translate-y-0.5 transition-transform"
                >
                  <div className="text-sm font-bold text-gray-900 group-hover:text-ibdn-primary transition-colors">
                    {empresa.razao_social}
                  </div>
                  <div className="text-xs text-gray-500 mt-0.5">
                    {empresa.nome_fantasia || "-"}
                  </div>
                </Link>
              </td>
              <td className="px-6 py-5 whitespace-nowrap">
                <div className="text-sm text-gray-600 font-mono bg-gray-50 px-2 py-1 rounded inline-block">{empresa.cnpj}</div>
              </td>
              <td className="px-6 py-5 whitespace-nowrap">
                {empresa.ativo ? (
                  <span className="px-3 py-1 inline-flex text-xs leading-5 font-bold rounded-full bg-green-100 text-green-800 border border-green-200">
                    Ativo
                  </span>
                ) : (
                  <span className="px-3 py-1 inline-flex text-xs leading-5 font-bold rounded-full bg-red-100 text-red-800 border border-red-200">
                    Inativo
                  </span>
                )}
              </td>
              <td className="px-6 py-5 whitespace-nowrap text-right text-sm font-medium">
                <div className="flex items-center justify-end space-x-3 opacity-70 group-hover:opacity-100 transition-opacity">
                  <button
                    onClick={() => onAssociateSelo(empresa.id)}
                    className="p-2 text-ibdn-accent hover:bg-ibdn-accent/10 rounded-lg transition-colors"
                    title="Associar Selo"
                  >
                    <Award className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => onEdit(empresa.id)}
                    className="p-2 text-gray-400 hover:text-ibdn-primary hover:bg-ibdn-primary/5 rounded-lg transition-colors"
                    title="Editar"
                  >
                    <Pencil className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => onDelete(empresa.id)}
                    className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Excluir"
                  >
                    <Trash2 className="w-5 h-5" />
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

export default EmpresasTable;
