import React, { useState, useEffect } from "react";
import * as seloService from "../services/seloService";
import SolicitacoesSeloTable from "../components/SolicitacoesSeloTable";

const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-10">
    <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-indigo-600"></div>
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
      window.confirm("Tem certeza que deseja aprovar esta solicitação de selo?")
    ) {
      try {
        await seloService.aprovarSelo(seloId);
        await fetchSolicitacoes(); // Refresh the list
        alert("Selo aprovado com sucesso!");
      } catch (err) {
        alert("Ocorreu um erro ao aprovar o selo.");
      }
    }
  };

  // NOTE: A 'reject' function would be added here. For now, we only have 'approve'.
  // const handleReject = async (seloId) => { ... }

  const renderContent = () => {
    if (loading) return <LoadingSpinner />;
    if (error)
      return (
        <div className="text-center p-10 bg-red-100 text-red-700 rounded-lg shadow">
          <h3 className="text-lg font-semibold">{error}</h3>
        </div>
      );
    return (
      <SolicitacoesSeloTable
        solicitacoes={solicitacoes}
        onApprove={handleApprove}
      />
    );
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">
          Solicitações de Selo
        </h1>
      </div>
      {renderContent()}
    </div>
  );
}

export default SolicitacoesSeloPage;
