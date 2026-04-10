import React from "react";
import { Pencil, Trash2, Settings } from "lucide-react";

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
    <>
      <div className="md:hidden space-y-4">
        {perfis.map((perfil) => (
          <div key={perfil.id} className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 flex flex-col gap-2 relative">
            <div className="flex justify-between items-start">
              <div className="text-base font-bold text-gray-900">{perfil.nome}</div>
            </div>
            <div className="text-sm text-gray-600 mt-1">
              <span className="font-medium text-gray-700 mr-2">Permissões atreladas:</span>
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
                {perfil.permissoes?.length || 0}
              </span>
            </div>
            <div className="flex flex-wrap items-center justify-end gap-2 mt-2 pt-3 border-t border-gray-50">
              <button
                onClick={() => onManagePermissions(perfil)}
                className="p-2 text-ibdn-primary bg-ibdn-primary/5 hover:bg-ibdn-primary/10 rounded-lg transition-colors flex-1 flex justify-center items-center font-medium text-sm"
                title="Gerir Permissões"
              >
                <Settings className="w-4 h-4 mr-1.5" /> Gerir
              </button>
              <button
                onClick={() => onEdit(perfil)}
                className="p-2 text-gray-500 bg-gray-50 hover:text-ibdn-primary rounded-lg transition-colors flex-1 flex justify-center items-center font-medium text-sm"
                title="Editar"
              >
                <Pencil className="w-4 h-4 mr-1.5" /> Editar
              </button>
              <button
                onClick={() => onDelete(perfil.id)}
                className="p-2 text-red-500 bg-red-50 hover:bg-red-100 rounded-lg transition-colors flex-1 flex justify-center items-center font-medium text-sm"
                title="Excluir"
              >
                <Trash2 className="w-4 h-4 mr-1.5" /> Excluir
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="hidden md:block overflow-x-auto premium-card bg-white rounded-3xl shadow-sm border border-gray-100">
        <table className="min-w-full divide-y divide-gray-100">
          <thead className="bg-ibdn-bg/50">
            <tr>
              <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest rounded-tl-3xl font-serif">
                Nome do Perfil
              </th>
              <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest font-serif">
                Permissões
              </th>
              <th scope="col" className="relative px-6 py-4 rounded-tr-3xl">
                <span className="sr-only">Ações</span>
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-50">
            {perfis.map((perfil) => (
              <tr key={perfil.id} className="hover:bg-ibdn-bg/30 transition-colors group">
                <td className="px-6 py-5 whitespace-nowrap">
                  <div className="text-sm font-bold text-gray-900 group-hover:text-ibdn-primary transition-colors">
                    {perfil.nome}
                  </div>
                </td>
                <td className="px-6 py-5 whitespace-nowrap">
                  <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                    {perfil.permissoes?.length || 0} vinculadas
                  </span>
                </td>
                <td className="px-6 py-5 whitespace-nowrap text-right text-sm font-medium">
                  <div className="flex items-center justify-end space-x-2 opacity-70 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => onManagePermissions(perfil)}
                      className="p-2 text-ibdn-primary bg-ibdn-primary/5 hover:bg-ibdn-primary/10 rounded-lg transition-colors cursor-pointer"
                      title="Gerir Permissões"
                    >
                      <Settings className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => onEdit(perfil)}
                      className="p-2 text-gray-400 hover:text-ibdn-primary hover:bg-ibdn-primary/5 rounded-lg transition-colors"
                      title="Editar"
                    >
                      <Pencil className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => onDelete(perfil.id)}
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

export default PerfisTable;
