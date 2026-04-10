import React from "react";

const formatDate = (dateString) => {
  if (!dateString) return "-";
  try {
    const date = new Date(dateString);
    const userTimezoneOffset = date.getTimezoneOffset() * 60000;
    return new Date(date.getTime() + userTimezoneOffset).toLocaleDateString(
      "pt-BR"
    );
  } catch (error) {
    return "Inválida";
  }
};

const getStatusClass = (status) => {
  switch (
    status.toLowerCase() // Usar toLowerCase para garantir a correspondência
  ) {
    case "ativo":
      return "bg-green-100 text-green-800";
    case "pendente":
      return "bg-yellow-100 text-yellow-800";
    case "expirado":
      return "bg-red-100 text-red-800";
    case "em renovação":
      return "bg-blue-100 text-blue-800";
    default:
      return "bg-gray-100 text-gray-800";
  }
};

function SelosAssociadosTable({ selos }) {
  if (!selos || selos.length === 0) {
    return (
      <div className="text-center p-6 bg-gray-50 rounded-lg">
        <h3 className="text-md font-semibold text-gray-600">
          Nenhum selo associado
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          Esta empresa ainda não possui selos ou nenhuma solicitação foi feita.
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
                <div className="text-base font-bold text-gray-900">{selo.nome_selo}</div>
                <div className="text-xs text-gray-500 font-mono bg-gray-50 px-2 py-1 rounded inline-block mt-1 w-fit">
                  {selo.sigla_selo || "Aguardando Aprovação"}
                </div>
              </div>
              <span className={`px-2 py-1 inline-flex text-xs font-bold rounded-full border capitalize ${getStatusClass(selo.status)}`}>
                {selo.status}
              </span>
            </div>
            <div className="text-sm text-gray-600 mt-1">
              {selo.data_expiracao ? `Expira em: ${formatDate(selo.data_expiracao)}` : "Validade: N/A"}
            </div>
          </div>
        ))}
      </div>

      <div className="hidden md:block overflow-x-auto premium-card bg-white rounded-3xl shadow-sm border border-gray-100">
        <table className="min-w-full divide-y divide-gray-100">
          <thead className="bg-ibdn-bg/50">
            <tr>
              <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest rounded-tl-3xl font-serif">
                Tipo de Selo
              </th>
              <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest font-serif">
                Código
              </th>
              <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest font-serif">
                Status
              </th>
              <th scope="col" className="px-6 py-4 text-left text-xs font-bold text-ibdn-earthy uppercase tracking-widest font-serif rounded-tr-3xl">
                Validade
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-50">
          {selos.map((selo) => (
            <tr key={selo.id} className="hover:bg-ibdn-bg/30 transition-colors group">
              <td className="px-6 py-5 whitespace-nowrap text-sm font-bold text-gray-900 group-hover:text-ibdn-primary transition-colors">
                {selo.nome_selo} ({selo.sigla_selo})
              </td>
              <td className="px-6 py-5 whitespace-nowrap">
                <div className="text-sm text-gray-500 font-mono bg-gray-50 px-2 py-1 rounded inline-block w-fit">
                  {selo.sigla_selo || "Aguardando Aprovação"}
                </div>
              </td>
              <td className="px-6 py-5 whitespace-nowrap">
                <span className={`px-3 py-1 inline-flex text-xs leading-5 font-bold rounded-full capitalize ${getStatusClass(selo.status)}`}>
                  {selo.status}
                </span>
              </td>
              <td className="px-6 py-5 whitespace-nowrap text-sm text-gray-900 font-medium">
                {selo.data_expiracao ? `Expira em: ${formatDate(selo.data_expiracao)}` : "N/A"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>
    </>
  );
}

export default SelosAssociadosTable;
