import React, { useState, useEffect } from "react";
import * as empresaService from "../services/empresaService";
import * as seloService from "../services/seloService"; // Importar serviço de selo
import EmpresasTable from "../components/EmpresasTable";
import Modal from "../components/Modal";
import EmpresaForm from "../components/EmpresaForm";
import AssociarSeloForm from "../components/AssociarSeloForm"; // Importar novo formulário

const LoadingSpinner = () => (
  <div className="flex flex-col justify-center items-center p-20 premium-card bg-white rounded-3xl shadow-sm border border-gray-100 my-8">
    <div className="w-12 h-12 border-4 border-ibdn-primary/20 border-t-ibdn-primary rounded-full animate-spin mb-4"></div>
    <p className="text-ibdn-primary font-medium opacity-80">Carregando dados...</p>
  </div>
);

function EmpresasPage() {
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [modalState, setModalState] = useState({
    isOpen: false,
    mode: null,
    data: null,
  });
  const [isSaving, setIsSaving] = useState(false);

  const fetchEmpresas = async () => {
    try {
      setLoading(true);
      const data = await empresaService.listarEmpresas();
      setEmpresas(data);
      setError(null);
    } catch (err) {
      setError(
        "Falha ao carregar os dados das empresas. Tente novamente mais tarde."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmpresas();
  }, []);

  const handleCloseModal = () => {
    if (isSaving) return;
    setModalState({ isOpen: false, mode: null, data: null });
  };

  // --- Funções para gerir Modais ---
  const handleOpenAddEmpresaModal = () =>
    setModalState({ isOpen: true, mode: "ADD_EDIT_EMPRESA", data: null });
  const handleOpenEditEmpresaModal = (empresaId) => {
    const empresaToEdit = empresas.find((e) => e.id === empresaId);
    setModalState({
      isOpen: true,
      mode: "ADD_EDIT_EMPRESA",
      data: empresaToEdit,
    });
  };
  const handleOpenAssociateSeloModal = (empresaId) => {
    setModalState({
      isOpen: true,
      mode: "ASSOCIATE_SELO",
      data: { empresaId },
    });
  };

  // --- Funções de Submissão ---
  const handleEmpresaFormSubmit = async (formData) => {
    setIsSaving(true);
    try {
      if (modalState.data?.id) {
        await empresaService.atualizarEmpresa(modalState.data.id, formData);
      } else {
        await empresaService.adicionarEmpresa(formData);
      }
      handleCloseModal();
      await fetchEmpresas();
    } catch (err) {
      alert("Não foi possível salvar a empresa.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleSeloFormSubmit = async (formData) => {
    setIsSaving(true);
    try {
      await seloService.associarSeloAEmpresa(
        modalState.data.empresaId,
        formData
      );
      alert("Selo associado com sucesso!");
      handleCloseModal();
    } catch (err) {
      alert("Não foi possível associar o selo.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("Tem a certeza que deseja excluir esta empresa?")) {
      try {
        await empresaService.excluirEmpresa(id);
        await fetchEmpresas();
      } catch (err) {
        alert("Não foi possível excluir a empresa.");
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
      <EmpresasTable
        empresas={empresas}
        onEdit={handleOpenEditEmpresaModal}
        onDelete={handleDelete}
        onAssociateSelo={handleOpenAssociateSeloModal}
      />
    );
  };

  const getModalTitle = () => {
    switch (modalState.mode) {
      case "ADD_EDIT_EMPRESA":
        return modalState.data?.id
          ? "Editar Empresa"
          : "Adicionar Nova Empresa";
      case "ASSOCIATE_SELO":
        return "Associar Novo Selo";
      default:
        return "";
    }
  };

  return (
    <div className="animate-fade-in-up space-y-8">
      <div className="flex justify-between items-end border-b border-gray-200 pb-5">
        <div>
          <h1 className="text-3xl font-serif font-bold text-ibdn-primary tracking-tight">Gerenciamento de Entidades</h1>
          <p className="mt-1 text-gray-500">Visualize, edite e acompanhe todas as empresas registradas.</p>
        </div>
        <button
          onClick={handleOpenAddEmpresaModal}
          className="inline-flex items-center justify-center px-5 py-2.5 bg-ibdn-primary text-white text-sm font-medium rounded-xl shadow-lg shadow-ibdn-primary/20 hover:bg-ibdn-primary-focus hover:-translate-y-0.5 transition-all duration-200"
        >
          Nova Empresa
        </button>
      </div>

      {renderContent()}

      <Modal
        isOpen={modalState.isOpen}
        onClose={handleCloseModal}
        title={getModalTitle()}
      >
        {modalState.mode === "ADD_EDIT_EMPRESA" && (
          <EmpresaForm
            initialData={modalState.data || {}}
            onSubmit={handleEmpresaFormSubmit}
            onCancel={handleCloseModal}
            isSaving={isSaving}
          />
        )}
        {modalState.mode === "ASSOCIATE_SELO" && (
          <AssociarSeloForm
            onSubmit={handleSeloFormSubmit}
            onCancel={handleCloseModal}
            isSaving={isSaving}
          />
        )}
      </Modal>
    </div>
  );
}

export default EmpresasPage;
