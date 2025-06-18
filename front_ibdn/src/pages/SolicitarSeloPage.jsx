import React, { useState, useEffect, useCallback } from "react";
import * as seloService from "../services/seloService";
import * as tipoSeloService from "../services/tipoSeloService";
import Modal from "../components/Modal";
import SolicitarSeloForm from "../components/SolicitarSeloForm";
import useAuthStore from "../store/authStore";

const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-10">
    <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-indigo-600"></div>
  </div>
);

function SolicitarSeloPage() {
  const { user } = useAuthStore();
  const [tiposSelo, setTiposSelo] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [solicitacoesDaEmpresa, setSolicitacoesDaEmpresa] = useState([]);

  const fetchTiposSeloAndSolicitacoes = useCallback(async () => {
    // Se o usuário não tiver uma empresa associada, não há o que buscar.
    if (!user?.empresa_id) {
      setLoading(false);
      return;
    }
    try {
      setLoading(true);
      const [tiposSeloData, solicitacoesData] = await Promise.all([
        tipoSeloService.listarTiposSelo(),
        seloService.getSelosByEmpresa(user.empresa_id),
      ]);
      setTiposSelo(tiposSeloData);
      // Filtra para exibir apenas as solicitações que estão aguardando alguma ação
      setSolicitacoesDaEmpresa(
        solicitacoesData.filter(
          (s) => s.status === "Pendente" || s.status === "Em Renovação"
        )
      );
      setError(null);
    } catch (err) {
      setError(
        "Falha ao carregar dados. Por favor, tente novamente mais tarde."
      );
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    fetchTiposSeloAndSolicitacoes();
  }, [fetchTiposSeloAndSolicitacoes]);

  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    if (isSaving) return;
    setIsModalOpen(false);
  };

  const handleSolicitarSelo = async (dadosSolicitacao) => {
    setIsSaving(true);
    try {
      // O serviço já espera o objeto completo { id_selo, plano_anos }
      await seloService.solicitarSelo(dadosSolicitacao);
      alert(
        "Solicitação de selo enviada com sucesso! Um administrador revisará sua solicitação."
      );
      handleCloseModal();
      await fetchTiposSeloAndSolicitacoes(); // Atualiza a lista de solicitações pendentes
    } catch (err) {
      const errorMessage =
        err.response?.data?.detail ||
        "Não foi possível enviar a solicitação. Verifique se você já possui este selo ou se a empresa está ativa.";
      alert(errorMessage);
      console.error("Erro ao solicitar selo:", err);
    } finally {
      setIsSaving(false);
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

    // Exibe uma mensagem se o usuário ainda não tiver cadastrado sua empresa
    if (!user?.empresa_id) {
      return (
        <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 rounded-lg shadow">
          <p className="font-semibold">Atenção:</p>
          <p>
            Você precisa ter uma empresa registrada para solicitar selos. Por
            favor, complete o cadastro da sua empresa no menu "Registrar
            Empresa".
          </p>
        </div>
      );
    }

    return (
      <div className="space-y-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Solicitar Novo Selo
          </h2>
          <p className="text-gray-600 mb-4">
            Selecione um tipo de selo do nosso catálogo para enviar uma
            solicitação de concessão para a sua empresa. Sua solicitação será
            revisada por um administrador.
          </p>
          <button
            onClick={handleOpenModal}
            className="px-4 py-2 bg-green-900 text-white font-semibold rounded-md shadow-sm hover:bg-green-700 disabled:opacity-50"
            disabled={tiposSelo.length === 0}
          >
            Solicitar Selo Agora
          </button>
          {tiposSelo.length === 0 && (
            <p className="mt-2 text-sm text-gray-500">
              Não há tipos de selo disponíveis para solicitação no momento. Por
              favor, volte mais tarde.
            </p>
          )}
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Minhas Solicitações Pendentes e em Renovação
          </h2>
          {solicitacoesDaEmpresa.length > 0 ? (
            <ul className="divide-y divide-gray-200">
              {solicitacoesDaEmpresa.map((solicitacao) => (
                <li
                  key={solicitacao.id}
                  className="py-3 flex justify-between items-center"
                >
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {solicitacao.nome_selo} (
                      <span className="font-mono">
                        {solicitacao.sigla_selo}
                      </span>
                      )
                    </p>
                    <p className="text-xs text-gray-600">
                      Status:{" "}
                      <span className="capitalize font-semibold">
                        {solicitacao.status}
                      </span>
                    </p>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-gray-500">
              Você não tem solicitações de selo pendentes ou em renovação para a
              sua empresa.
            </p>
          )}
        </div>
      </div>
    );
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Solicitar Selo</h1>
      </div>

      {renderContent()}

      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title="Formulário de Solicitação de Selo"
      >
        <SolicitarSeloForm
          tiposSelo={tiposSelo}
          onSubmit={handleSolicitarSelo}
          onCancel={handleCloseModal}
          isSaving={isSaving}
        />
      </Modal>
    </div>
  );
}

export default SolicitarSeloPage;
