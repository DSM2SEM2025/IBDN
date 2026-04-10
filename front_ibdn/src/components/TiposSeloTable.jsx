// src/components/TiposSeloTable.jsx
import React from "react";
import { Pencil, Trash2 } from "lucide-react";

function TiposSeloTable({ tiposSelo, onEdit, onDelete }) {
  if (!tiposSelo || tiposSelo.length === 0) {
    return (
      <div className="text-center p-10 bg-white rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-700">
          Nenhum tipo de selo encontrado
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          Comece por adicionar um novo tipo de selo.
        </p>
      </div>
    );
  }

  return (
    <>
      {/* Visão Mobile */}
      <div className="md:hidden space-y-4">
        {tiposSelo.map((selo) => (
          <div key={selo.id} className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 flex flex-col gap-2 relative">
            <div className="flex justify-between items-start">
              <div className="flex flex-col">
                <div className="text-base font-bold text-gray-900">{selo.nome}</div>
                <div className="text-xs text-gray-500 font-mono bg-gray-50 px-2 py-1 rounded inline-block mt-1 w-fit">
                  {selo.sigla}
                </div>
              </div>
            </div>
            <div className="text-sm text-gray-600 mt-2">
              {selo.descricao}
            </div>
            <div className="flex items-center justify-end space-x-2 mt-2 pt-3 border-t border-gray-50">
              <button
                onClick={() => onEdit(selo)}
                className="p-2 text-gray-500 bg-gray-50 hover:text-ibdn-primary rounded-lg transition-colors flex-1 flex justify-center items-center font-medium text-sm"
                title="Editar"
              >
                <Pencil className="w-4 h-4 mr-1.5" /> Editar
              </button>
              <button
                onClick={() => onDelete(selo.id)}
                className="p-2 text-red-500 bg-red-50 hover:bg-red-100 rounded-lg transition-colors flex-1 flex justify-center items-center font-medium text-sm"
                title="Excluir"
              >
                <Trash2 className="w-4 h-4 mr-1.5" /> Excluir
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Visão Desktop */}
      <div className="hidden md:block overflow-x-auto premium-card bg-white rounded-3xl shadow-sm border border-gray-100">
        <table className="min-w-full divide-y divide-gray-100">
          <thead className="bg-ibdn-bg/50">
            <tr>
              <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest rounded-tl-3xl font-serif">
                Nome
              </th>
              <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest font-serif">
                Sigla
              </th>
              <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest font-serif">
                Descrição
              </th>
              <th scope="col" className="relative px-6 py-4 rounded-tr-3xl">
                <span className="sr-only">Ações</span>
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-50">
            {tiposSelo.map((selo) => (
              <tr key={selo.id} className="hover:bg-ibdn-bg/30 transition-colors group">
                <td className="px-6 py-5 whitespace-nowrap">
                  <div className="text-sm font-bold text-gray-900 group-hover:text-ibdn-primary transition-colors">
                    {selo.nome}
                  </div>
                </td>
                <td className="px-6 py-5 whitespace-nowrap">
                  <div className="text-sm text-gray-600 font-mono bg-gray-50 px-2 py-1 rounded inline-block">
                    {selo.sigla}
                  </div>
                </td>
                <td className="px-6 py-5 text-sm text-gray-600 font-medium">
                  {selo.descricao}
                </td>
                <td className="px-6 py-5 whitespace-nowrap text-right text-sm font-medium">
                  <div className="flex items-center justify-end space-x-2 opacity-70 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => onEdit(selo)}
                      className="p-2 text-gray-400 hover:text-ibdn-primary hover:bg-ibdn-primary/5 rounded-lg transition-colors"
                      title="Editar"
                    >
                      <Pencil className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => onDelete(selo.id)}
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

export default TiposSeloTable;
