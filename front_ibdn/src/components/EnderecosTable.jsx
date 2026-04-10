import React from "react";
import { Pencil } from "lucide-react";

/**
 * Componente para exibir uma tabela de endereços de uma empresa.
 * @param {Object} props
 * @param {Array} props.enderecos - A lista de endereços a ser exibida.
 * @param {Function} props.onEdit - Função a ser chamada ao clicar no botão de editar.
 */
function EnderecosTable({ enderecos, onEdit }) {
  if (!enderecos || enderecos.length === 0) {
    return (
      <div className="text-center p-6 bg-gray-50 rounded-lg">
        <h3 className="text-md font-semibold text-gray-600">
          Nenhum endereço encontrado
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          Esta empresa ainda não possui endereços registados.
        </p>
      </div>
    );
  }

  return (
    <>
      {/* Visão Mobile */}
      <div className="md:hidden space-y-4">
        {enderecos.map((endereco) => (
          <div key={endereco.id} className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 flex flex-col gap-2 relative">
            <div className="text-base font-bold text-gray-900">{endereco.logradouro}</div>
            <div className="text-sm text-gray-500">{endereco.complemento || "Sem complemento"}</div>
            <div className="flex flex-wrap gap-2 text-sm text-gray-700 mt-2">
              <span className="bg-gray-50 px-2 py-1 rounded">{endereco.bairro}</span>
              <span className="bg-gray-50 px-2 py-1 rounded">{endereco.cidade} - {endereco.uf}</span>
              <span className="bg-gray-50 px-2 py-1 rounded font-mono">{endereco.cep}</span>
            </div>
            <div className="flex justify-end pt-3 mt-1 border-t border-gray-50">
              <button
                onClick={() => onEdit(endereco)}
                className="p-2 text-gray-500 bg-gray-50 hover:text-ibdn-primary hover:bg-ibdn-primary/5 rounded-lg flex items-center flex-1 justify-center transition-colors"
                title="Editar Endereço"
              >
                <Pencil className="w-4 h-4 mr-2" /> Editar
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
                Logradouro
              </th>
              <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest font-serif">
                Bairro
              </th>
              <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest font-serif">
                Cidade / UF
              </th>
              <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest font-serif">
                CEP
              </th>
              <th scope="col" className="relative px-6 py-4 rounded-tr-3xl">
                <span className="sr-only">Ações</span>
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-50">
          {enderecos.map((endereco) => (
            <tr key={endereco.id} className="hover:bg-ibdn-bg/30 transition-colors group">
              <td className="px-6 py-5 whitespace-nowrap">
                <div className="text-sm font-bold text-gray-900 group-hover:text-ibdn-primary transition-colors">
                  {endereco.logradouro}
                </div>
                <div className="text-sm text-gray-500 mt-0.5">
                  {endereco.complemento || "Sem complemento"}
                </div>
              </td>
              <td className="px-6 py-5 whitespace-nowrap">
                <div className="text-sm text-gray-600 font-medium bg-gray-50 px-2 py-1 rounded inline-block">{endereco.bairro}</div>
              </td>
              <td className="px-6 py-5 whitespace-nowrap">
                <div className="text-sm text-gray-900">
                  {endereco.cidade} - {endereco.uf}
                </div>
              </td>
              <td className="px-6 py-5 whitespace-nowrap">
                <div className="text-sm text-gray-600 font-mono bg-gray-50 px-2 py-1 rounded inline-block">{endereco.cep}</div>
              </td>
              <td className="px-6 py-5 whitespace-nowrap text-right text-sm font-medium">
                <div className="opacity-70 group-hover:opacity-100 transition-opacity">
                  <button
                    onClick={() => onEdit(endereco)}
                    className="p-2 text-gray-400 hover:text-ibdn-primary hover:bg-ibdn-primary/5 rounded-lg transition-colors"
                    title="Editar Endereço"
                  >
                    <Pencil className="w-5 h-5" />
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

export default EnderecosTable;
