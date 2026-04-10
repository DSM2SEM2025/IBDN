import React, { useState, useEffect } from "react";
import * as seloService from "../services/seloService";
import SolicitacoesSeloTable from "../components/SolicitacoesSeloTable";

const LoadingSpinner = () => (
  <div className="flex flex-col justify-center items-center p-20 premium-card bg-white rounded-3xl shadow-sm border border-gray-100 my-8">
    <div className="w-12 h-12 border-4 border-ibdn-primary/20 border-t-ibdn-primary rounded-full animate-spin mb-4"></div>
    <p className="text-ibdn-primary font-medium opacity-80">Carregando dados...</p>
  </div>
);

function SolicitacoesSeloPage() {
  const [solicitacoes, setSolicitacoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchSolicitacoes = async () => {
    try {
      setLoading(true);
      const data = await seloService.getSolicitacoesSelo();
      setSolicitacoes(data);
      setError(null);
    } catch (err) {
      setError("Falha ao carregar as solicitações de selo.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSolicitacoes();
  }, []);

  const handleApprove = async (seloId) => {
    if (
      window.confirm("Tem certeza que deseja APROVAR esta solicitação de selo?")
    ) {
      try {
        await seloService.aprovarSelo(seloId);
        await fetchSolicitacoes();
        alert("Selo aprovado com sucesso!");
      } catch (err) {
        alert("Ocorreu um erro ao aprovar o selo.");
      }
    }
  };

  // --- NOVA FUNÇÃO PARA RECUSAR ---
  const handleReject = async (seloId) => {
    if (
      window.confirm("Tem certeza que deseja RECUSAR esta solicitação de selo?")
    ) {
      try {
        await seloService.recusarSelo(seloId);
        await fetchSolicitacoes(); // Atualiza a lista após a recusa
        alert("Solicitação de selo recusada com sucesso.");
      } catch (err) {
        alert("Ocorreu um erro ao recusar a solicitação.");
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
      <SolicitacoesSeloTable
        solicitacoes={solicitacoes}
        onApprove={handleApprove}
        onReject={handleReject} // Passando a nova função para a tabela
      />
    );
  };

  return (
    <div className="animate-fade-in-up space-y-8">
      <div className="flex justify-between items-end border-b border-gray-200 pb-5">
        <div>
          <h1 className="text-3xl font-serif font-bold text-ibdn-primary tracking-tight">
            Validação de Solicitações
          </h1>
          <p className="mt-1 text-gray-500">Avalie e aprove novos selos requisitados pelas empresas.</p>
        </div>
      </div>
      {renderContent()}
    </div>
  );
}

export default SolicitacoesSeloPage;
