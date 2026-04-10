import React, { useState, useEffect, useMemo } from "react";
import * as seloService from "../services/seloService";
import SelosTable from "../components/SelosTable";

const LoadingSpinner = () => (
  <div className="flex flex-col justify-center items-center p-20 premium-card bg-white rounded-3xl shadow-sm border border-gray-100 my-8">
    <div className="w-12 h-12 border-4 border-ibdn-primary/20 border-t-ibdn-primary rounded-full animate-spin mb-4"></div>
    <p className="text-ibdn-primary font-medium opacity-80">Carregando dados...</p>
  </div>
);

// Helper para formatar a data string (YYYY-MM-DD) para o formato local (DD/MM/YYYY).
const formatDate = (dateString) => {
  if (!dateString) return "-";
  try {
    const date = new Date(dateString);
    // Adiciona o fuso horário para corrigir a exibição da data que vem como UTC
    const userTimezoneOffset = date.getTimezoneOffset() * 60000;
    return new Date(date.getTime() + userTimezoneOffset).toLocaleDateString(
      "pt-BR"
    );
  } catch (error) {
    console.error("Data inválida:", dateString, error);
    return "Inválida";
  }
};

function SelosPage() {
  const [selos, setSelos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Função para carregar ou recarregar os dados da tabela
  const fetchSelos = async () => {
    try {
      setLoading(true);
      const data = await seloService.listarTodosSelos();
      // A API pode retornar um objeto com uma chave `dados`
      setSelos(Array.isArray(data.dados) ? data.dados : []);
      setError(null);
    } catch (err) {
      setError(
        "Falha ao carregar os dados dos selos. Tente novamente mais tarde."
      );
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSelos();
  }, []);

  // Mapeia os dados da API para um formato ideal para a tabela de visualização
  // useMemo evita que o mapeamento seja refeito a cada renderização, apenas quando `selos` mudar.
  const selosMapeados = useMemo(() => {
    return selos.map((selo) => ({
      id: selo.id,
      codigo: selo.sigla_selo,
      status: selo.status,
      empresa: {
        razao_social: selo.razao_social || "N/A",
      },
      data_emissao: formatDate(selo.data_emissao),
      data_validade: formatDate(selo.data_expiracao),
    }));
  }, [selos]);

  // --- Funções para as Ações ---
  const handleApprove = async (seloId) => {
    if (window.confirm("Tem a certeza que deseja aprovar este selo?")) {
      try {
        await seloService.aprovarSelo(seloId);
        await fetchSelos(); // Recarrega a lista para mostrar o novo status
      } catch (err) {
        alert("Ocorreu um erro ao aprovar o selo.");
      }
    }
  };

  const handleRenew = async (seloId) => {
    if (
      window.confirm(
        "Tem a certeza que deseja solicitar a renovação para este selo?"
      )
    ) {
      try {
        await seloService.solicitarRenovacaoSelo(seloId);
        alert("Pedido de renovação enviado com sucesso!");
        await fetchSelos();
      } catch (err) {
        alert("Ocorreu um erro ao solicitar a renovação.");
      }
    }
  };

  const renderContent = () => {
    if (loading) return <LoadingSpinner />;
    if (error)
      return (
        <div className="text-center p-14 premium-card bg-red-50 rounded-3xl shadow-sm border border-red-100 flex flex-col items-center my-8">
          <div className="w-16 h-16 rounded-full bg-red-100 flex items-center justify-center mb-4">
            <svg className="w-8 h-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 className="text-xl font-serif font-bold text-red-800">Erro</h3>
          <p className="mt-2 text-md text-red-600 max-w-sm">{error}</p>
        </div>
      );
    return (
      <SelosTable
        selos={selosMapeados} // Passa os dados já mapeados para a tabela
        onApprove={handleApprove}
        onRenew={handleRenew}
      />
    );
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Gerir Selos</h1>
        {/* O botão para adicionar selo foi implementado na página de empresas */}
      </div>

      {renderContent()}
    </div>
  );
}

export default SelosPage;
