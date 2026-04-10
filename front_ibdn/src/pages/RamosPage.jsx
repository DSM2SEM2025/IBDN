import React, { useState, useEffect } from "react";
import * as ramoService from "../services/ramoService";
import RamosTable from "../components/RamosTable";
import Modal from "../components/Modal";
import RamoForm from "../components/RamoForm";

const LoadingSpinner = () => (
  <div className="flex flex-col justify-center items-center p-20 premium-card bg-white rounded-3xl shadow-sm border border-gray-100 my-8">
    <div className="w-12 h-12 border-4 border-ibdn-primary/20 border-t-ibdn-primary rounded-full animate-spin mb-4"></div>
    <p className="text-ibdn-primary font-medium opacity-80">Carregando dados...</p>
  </div>
);

function RamosPage() {
  const [ramos, setRamos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Estados para o modal e formulário
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingRamo, setEditingRamo] = useState(null);
  const [isSaving, setIsSaving] = useState(false);

  // Função para carregar ou recarregar os dados da tabela
  const fetchRamos = async () => {
    try {
      setLoading(true);
      const data = await ramoService.listarRamos();
      setRamos(data);
      setError(null);
    } catch (err) {
      setError(
        "Falha ao carregar os dados dos ramos. Tente novamente mais tarde. " +
          err.message
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRamos();
  }, []);

  // --- Funções para gerir o Modal ---
  const handleOpenModalForAdd = () => {
    setEditingRamo(null);
    setIsModalOpen(true);
  };

  const handleOpenModalForEdit = (ramo) => {
    setEditingRamo(ramo);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    if (isSaving) return;
    setIsModalOpen(false);
    setEditingRamo(null);
  };

  // --- Funções para submeter e excluir ---
  const handleFormSubmit = async (formData) => {
    setIsSaving(true);
    try {
      if (editingRamo) {
        await ramoService.atualizarRamo(editingRamo.id, formData);
      } else {
        await ramoService.criarRamo(formData);
      }
      handleCloseModal();
      await fetchRamos(); // Recarrega a lista
    } catch (submitError) {
      console.error("Erro ao salvar ramo:", submitError);
      alert(
        "Não foi possível salvar o ramo. Verifique o console para mais detalhes."
      );
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("Tem a certeza que deseja excluir este ramo?")) {
      try {
        await ramoService.deletarRamo(id);
        await fetchRamos(); // Recarrega a lista
      } catch (deleteError) {
        console.error("Erro ao excluir ramo:", deleteError);
        alert("Não foi possível excluir o ramo.");
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
      <RamosTable
        ramos={ramos}
        onEdit={handleOpenModalForEdit}
        onDelete={handleDelete}
      />
    );
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">
          Gerir Ramos de Atividade
        </h1>
        <button
          onClick={handleOpenModalForAdd}
          className="px-4 py-2 bg-green-900 text-white font-semibold rounded-md shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Adicionar Ramo
        </button>
      </div>

      {renderContent()}

      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title={editingRamo ? "Editar Ramo" : "Adicionar Novo Ramo"}
      >
        <RamoForm
          initialData={editingRamo || {}}
          onSubmit={handleFormSubmit}
          onCancel={handleCloseModal}
          isSaving={isSaving}
        />
      </Modal>
    </div>
  );
}

export default RamosPage;
