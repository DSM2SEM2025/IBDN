import React from "react";

// Reutilizando o ícone de edição
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
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Logradouro
            </th>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Bairro
            </th>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Cidade / UF
            </th>
            <th
              scope="col"
              className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              CEP
            </th>
            <th scope="col" className="relative px-6 py-3">
              <span className="sr-only">Ações</span>
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {enderecos.map((endereco) => (
            <tr
              key={endereco.id}
              className="hover:bg-gray-50 transition-colors"
            >
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm font-medium text-gray-900">
                  {endereco.logradouro}
                </div>
                <div className="text-sm text-gray-500">
                  {endereco.complemento || "Sem complemento"}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm text-gray-900">{endereco.bairro}</div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm text-gray-900">
                  {endereco.cidade} - {endereco.uf}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm text-gray-900">{endereco.cep}</div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button
                  onClick={() => onEdit(endereco)}
                  className="text-indigo-600 hover:text-indigo-900"
                  title="Editar Endereço"
                >
                  <EditIcon className="w-5 h-5" />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default EnderecosTable;
