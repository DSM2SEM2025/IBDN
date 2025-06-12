import React, { useState, useEffect } from "react";
import * as empresaService from "../services/empresaService";
import EmpresasTable from "../components/EmpresasTable";
import Modal from "../components/Modal";
import EmpresaForm from "../components/EmpresaForm";

const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-10">
    <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-indigo-600"></div>
  </div>
);

function EmpresasPage() {
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingEmpresa, setEditingEmpresa] = useState(null);
  const [isSaving, setIsSaving] = useState(false);

  const fetchEmpresas = async () => {
    try {
      setLoading(true);
      const data = await empresaService.listarEmpresas();
      setEmpresas(data);
      setError(null);
    } catch (err) {
      setError(
        `Falha ao carregar os dados das empresas. Tente novamente mais tarde. Erro: ${err.message}`
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmpresas();
  }, []);

  const handleOpenModalForAdd = () => {
    setEditingEmpresa(null);
    setIsModalOpen(true);
  };

  const handleOpenModalForEdit = (empresaId) => {
    const empresaToEdit = empresas.find((e) => e.id === empresaId);
    setEditingEmpresa(empresaToEdit);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    if (isSaving) return;
    setIsModalOpen(false);
    setEditingEmpresa(null);
  };

  const handleFormSubmit = async (formData) => {
    setIsSaving(true);
    try {
      if (editingEmpresa) {
        await empresaService.atualizarEmpresa(editingEmpresa.id, formData);
      } else {
        await empresaService.adicionarEmpresa(formData);
      }
      handleCloseModal();
      await fetchEmpresas(); // Recarrega a lista para mostrar as alterações
    } catch (submitError) {
      console.error("Erro ao salvar empresa:", submitError);
      alert(
        "Não foi possível salvar a empresa. Verifique o console para mais detalhes."
      );
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("Tem a certeza que deseja excluir esta empresa?")) {
      try {
        await empresaService.excluirEmpresa(id);
        await fetchEmpresas(); // Recarrega a lista
      } catch (deleteError) {
        console.error("Erro ao excluir empresa:", deleteError);
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
        onEdit={handleOpenModalForEdit}
        onDelete={handleDelete}
      />
    );
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Gerir Empresas</h1>
        <button
          onClick={handleOpenModalForAdd}
          className="px-4 py-2 bg-indigo-600 text-white font-semibold rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Adicionar Empresa
        </button>
      </div>

      {renderContent()}

      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title={editingEmpresa ? "Editar Empresa" : "Adicionar Nova Empresa"}
      >
        <EmpresaForm
          initialData={editingEmpresa || {}}
          onSubmit={handleFormSubmit}
          onCancel={handleCloseModal}
          isSaving={isSaving}
        />
      </Modal>
    </div>
  );
}

export default EmpresasPage;
