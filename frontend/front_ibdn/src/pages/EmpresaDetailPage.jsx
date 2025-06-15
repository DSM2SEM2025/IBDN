import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import * as empresaService from "../services/empresaService";
import * as empresaRamoService from "../services/empresaRamoService";
import * as ramoService from "../services/ramoService";
import * as enderecoService from "../services/enderecoService";
import * as notificacaoService from "../services/notificacaoService";
// NEW: Import seloService
import * as seloService from "../services/seloService";

import Modal from "../components/Modal";
import AssociarRamosForm from "../components/AssociarRamosForm";
import EnderecosTable from "../components/EnderecosTable";
import EnderecoForm from "../components/EnderecoForm";
import NotificacoesList from "../components/NotificacoesList";
import NotificacaoForm from "../components/NotificacaoForm";
// NEW: Import the new table component
import SelosAssociadosTable from "../components/SelosAssociadosTable";

const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-10">
    <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-indigo-600"></div>
  </div>
);

function EmpresaDetailPage() {
  const { empresaId } = useParams();
  const [empresa, setEmpresa] = useState(null);
  const [ramosAtuais, setRamosAtuais] = useState([]);
  const [todosOsRamos, setTodosOsRamos] = useState([]);
  const [enderecos, setEnderecos] = useState([]);
  const [notificacoes, setNotificacoes] = useState([]);
  // NEW: State for associated seals
  const [selos, setSelos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [modalState, setModalState] = useState({
    isOpen: false,
    mode: null,
    data: null,
  });
  const [isSaving, setIsSaving] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [
        empresaData,
        ramosAtuaisData,
        todosOsRamosData,
        enderecosData,
        notificacoesData,
        // NEW: Fetch associated seals
        selosData,
      ] = await Promise.all([
        empresaService.buscarEmpresaPorId(empresaId),
        empresaRamoService.getRamosPorEmpresa(empresaId),
        ramoService.listarRamos(),
        enderecoService.listarEnderecosDaEmpresa(empresaId),
        notificacaoService.listarNotificacoesEmpresa(empresaId),
        // NEW: Call the service function
        seloService.getSelosByEmpresa(empresaId),
      ]);
      setEmpresa(empresaData);
      setRamosAtuais(ramosAtuaisData);
      setTodosOsRamos(todosOsRamosData);
      setEnderecos(enderecosData);
      setNotificacoes(notificacoesData);
      // NEW: Set the state for seals
      setSelos(selosData);
      setError(null);
    } catch (err) {
      setError("Falha ao carregar os dados da empresa.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [empresaId]);

  const handleCloseModal = () =>
    !isSaving && setModalState({ isOpen: false, mode: null, data: null });
  const handleOpenRamosModal = () =>
    setModalState({ isOpen: true, mode: "MANAGE_RAMOS" });
  const handleOpenEditEnderecoModal = (endereco) =>
    setModalState({ isOpen: true, mode: "EDIT_ENDERECO", data: endereco });
  const handleOpenAddNotificacaoModal = () =>
    setModalState({ isOpen: true, mode: "ADD_NOTIFICACAO" });

  const handleSaveRamos = async (selectedRamosIds) => {
    setIsSaving(true);
    try {
      await empresaRamoService.atrelarRamosAEmpresa(
        empresaId,
        selectedRamosIds
      );
      handleCloseModal();
      await fetchData();
    } catch (err) {
      alert("Ocorreu um erro ao salvar os ramos.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleEnderecoFormSubmit = async (formData) => {
    setIsSaving(true);
    try {
      await enderecoService.atualizarEnderecoDaEmpresa(
        empresaId,
        modalState.data.id,
        formData
      );
      handleCloseModal();
      await fetchData();
    } catch (err) {
      alert("Ocorreu um erro ao atualizar o endereço.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleNotificacaoFormSubmit = async (formData) => {
    setIsSaving(true);
    try {
      await notificacaoService.criarNotificacao(empresaId, formData);
      handleCloseModal();
      await fetchData();
    } catch (err) {
      alert("Ocorreu um erro ao criar a notificação.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleMarkAsRead = async (notificacaoId) => {
    try {
      await notificacaoService.atualizarNotificacao(notificacaoId, {
        lida: true,
      });
      await fetchData();
    } catch (err) {
      alert("Erro ao marcar notificação como lida.");
    }
  };

  const handleDeleteNotificacao = async (notificacaoId) => {
    if (window.confirm("Tem a certeza que deseja excluir esta notificação?")) {
      try {
        await notificacaoService.deletarNotificacao(notificacaoId);
        await fetchData();
      } catch (err) {
        alert("Erro ao excluir notificação.");
      }
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error)
    return (
      <div className="text-center p-10 bg-red-100 text-red-700 rounded-lg shadow">
        <h3 className="text-lg font-semibold">{error}</h3>
        <Link
          to="/empresas"
          className="mt-4 inline-block text-indigo-600 hover:text-indigo-800"
        >
          &larr; Voltar para a lista
        </Link>
      </div>
    );

  const getModalTitle = () => {
    switch (modalState.mode) {
      case "MANAGE_RAMOS":
        return "Gerir Ramos da Empresa";
      case "EDIT_ENDERECO":
        return "Editar Endereço";
      case "ADD_NOTIFICACAO":
        return "Enviar Nova Notificação";
      default:
        return "";
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <Link
          to="/empresas"
          className="text-sm font-medium text-indigo-600 hover:text-indigo-800"
        >
          &larr; Voltar para a lista de empresas
        </Link>
      </div>
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">
          {empresa.razao_social}
        </h1>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold text-gray-800 border-b pb-3 mb-4">
          Detalhes da Empresa
        </h2>
        {/* ... existing company details grid ... */}
      </div>

      {/* NEW: Section to display associated seals */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold text-gray-800 border-b pb-3 mb-4">
          Selos Associados
        </h2>
        <SelosAssociadosTable selos={selos} />
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold text-gray-800 border-b pb-3 mb-4">
          Endereços
        </h2>
        <EnderecosTable
          enderecos={enderecos}
          onEdit={handleOpenEditEnderecoModal}
        />
      </div>

      {/* ... rest of the page (Ramos, Notificações, Modal) ... */}

      <Modal
        isOpen={modalState.isOpen}
        onClose={handleCloseModal}
        title={getModalTitle()}
      >
        {modalState.mode === "MANAGE_RAMOS" && (
          <AssociarRamosForm
            ramosAtuais={ramosAtuais}
            todosOsRamos={todosOsRamos}
            onSave={handleSaveRamos}
            onCancel={handleCloseModal}
            isSaving={isSaving}
          />
        )}
        {modalState.mode === "EDIT_ENDERECO" && (
          <EnderecoForm
            initialData={modalState.data}
            onSubmit={handleEnderecoFormSubmit}
            onCancel={handleCloseModal}
            isSaving={isSaving}
          />
        )}
        {modalState.mode === "ADD_NOTIFICACAO" && (
          <NotificacaoForm
            onSubmit={handleNotificacaoFormSubmit}
            onCancel={handleCloseModal}
            isSaving={isSaving}
          />
        )}
      </Modal>
    </div>
  );
}

export default EmpresaDetailPage;
