import React, { useState, useEffect } from "react";
import * as seloService from "../services/seloService";
import SelosTable from "../components/SelosTable";

const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-10">
    <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-indigo-600"></div>
  </div>
);

function SelosPage() {
  const [selos, setSelos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Função para carregar ou recarregar os dados da tabela
  const fetchSelos = async () => {
    try {
      setLoading(true);
      const data = await seloService.listarTodosSelos();
      // A API pode retornar um objeto com uma chave, vamos garantir que estamos a passar um array
      setSelos(Array.isArray(data) ? data : []);
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
        <div className="text-center p-10 bg-red-100 text-red-700 rounded-lg shadow">
          <h3 className="text-lg font-semibold">{error}</h3>
        </div>
      );
    return (
      <SelosTable
        selos={selos}
        onApprove={handleApprove}
        onRenew={handleRenew}
      />
    );
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Gerir Selos</h1>
        {/* O botão para adicionar selo será implementado na página de empresas */}
      </div>

      {renderContent()}
    </div>
  );
}

export default SelosPage;
