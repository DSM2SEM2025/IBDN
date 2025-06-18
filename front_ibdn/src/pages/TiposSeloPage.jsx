// src/pages/TiposSeloPage.jsx
import React, { useState, useEffect } from "react";
import * as tipoSeloService from "../services/tipoSeloService";
import TiposSeloTable from "../components/TiposSeloTable";
import Modal from "../components/Modal";
import TipoSeloForm from "../components/TipoSeloForm";

const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-10">
    <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-indigo-600"></div>
  </div>
);

function TiposSeloPage() {
  const [tiposSelo, setTiposSelo] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Estados para o modal
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingSelo, setEditingSelo] = useState(null);
  const [isSaving, setIsSaving] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const data = await tipoSeloService.listarTiposSelo();
      setTiposSelo(data);
      setError(null);
    } catch (err) {
      setError("Falha ao carregar os tipos de selo. Tente novamente.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleOpenAddModal = () => {
    setEditingSelo(null);
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (selo) => {
    setEditingSelo(selo);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    if (isSaving) return;
    setIsModalOpen(false);
    setEditingSelo(null);
  };

  const handleFormSubmit = async (formData) => {
    setIsSaving(true);
    try {
      if (editingSelo) {
        await tipoSeloService.atualizarTipoSelo(editingSelo.id, formData);
      } else {
        await tipoSeloService.criarTipoSelo(formData);
      }
      handleCloseModal();
      await fetchData(); // Recarrega a lista
    } catch (submitError) {
      alert("Não foi possível salvar o tipo de selo.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async (id) => {
    // CORREÇÃO: A mensagem agora reflete a ação de inativar.
    if (
      window.confirm(
        "Tem a certeza que deseja INATIVAR este tipo de selo? Ele não poderá ser usado para novas associações, mas o histórico será mantido."
      )
    ) {
      try {
        await tipoSeloService.deletarTipoSelo(id); // O serviço/endpoint continua o mesmo
        await fetchData(); // Recarrega a lista
      } catch (deleteError) {
        alert("Não foi possível inativar o tipo de selo.");
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
      <TiposSeloTable
        tiposSelo={tiposSelo}
        onEdit={handleOpenEditModal}
        onDelete={handleDelete}
      />
    );
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">
          Gerir Tipos de Selo
        </h1>
        <button
          onClick={handleOpenAddModal}
          className="px-4 py-2 bg-green-900 text-white font-semibold rounded-md shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Adicionar Tipo de Selo
        </button>
      </div>

      {renderContent()}

      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title={
          editingSelo ? "Editar Tipo de Selo" : "Adicionar Novo Tipo de Selo"
        }
      >
        <TipoSeloForm
          initialData={editingSelo || {}}
          onSubmit={handleFormSubmit}
          onCancel={handleCloseModal}
          isSaving={isSaving}
        />
      </Modal>
    </div>
  );
}

export default TiposSeloPage;
