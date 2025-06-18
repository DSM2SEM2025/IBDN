import React, { useState, useEffect } from "react";
import * as empresaService from "../services/empresaService";
import * as seloService from "../services/seloService"; // Importar serviço de selo
import EmpresasTable from "../components/EmpresasTable";
import Modal from "../components/Modal";
import EmpresaForm from "../components/EmpresaForm";
import AssociarSeloForm from "../components/AssociarSeloForm"; // Importar novo formulário

const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-10">
    <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-indigo-600"></div>
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
        <div className="text-center p-10 bg-red-100 text-red-700 rounded-lg shadow">
          <h3 className="text-lg font-semibold">{error}</h3>
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
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Gerir Empresas</h1>
        <button
          onClick={handleOpenAddEmpresaModal}
          className="px-4 py-2 bg-green-900 text-white font-semibold rounded-md shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Adicionar Empresa
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
