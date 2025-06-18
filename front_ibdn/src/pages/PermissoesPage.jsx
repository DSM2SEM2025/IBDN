import React, { useState, useEffect } from "react";
import * as permissaoService from "../services/permissaoService";
import PermissoesTable from "../components/PermissoesTable";
import Modal from "../components/Modal";
import PermissaoForm from "../components/PermissaoForm";

const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-10">
    <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-indigo-600"></div>
  </div>
);

function PermissoesPage() {
  const [permissoes, setPermissoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Estados para o modal e formulário
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingPermissao, setEditingPermissao] = useState(null);
  const [isSaving, setIsSaving] = useState(false);

  // Função para carregar ou recarregar os dados da tabela
  const fetchPermissoes = async () => {
    try {
      setLoading(true);
      const data = await permissaoService.listarPermissoes();
      setPermissoes(data);
      setError(null);
    } catch (err) {
      setError(
        "Falha ao carregar os dados das permissões. Tente novamente mais tarde." +
          err.message
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPermissoes();
  }, []);

  // --- Funções para gerir o Modal ---
  const handleOpenModalForAdd = () => {
    setEditingPermissao(null);
    setIsModalOpen(true);
  };

  const handleOpenModalForEdit = (permissao) => {
    setEditingPermissao(permissao);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    if (isSaving) return;
    setIsModalOpen(false);
    setEditingPermissao(null);
  };

  // --- Funções para submeter e excluir ---
  const handleFormSubmit = async (formData) => {
    setIsSaving(true);
    try {
      if (editingPermissao) {
        await permissaoService.atualizarPermissao(
          editingPermissao.id,
          formData
        );
      } else {
        await permissaoService.criarPermissao(formData);
      }
      handleCloseModal();
      await fetchPermissoes(); // Recarrega a lista
    } catch (submitError) {
      console.error("Erro ao salvar permissão:", submitError);
      alert(
        "Não foi possível salvar a permissão. Verifique o console para mais detalhes."
      );
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("Tem a certeza que deseja excluir esta permissão?")) {
      try {
        await permissaoService.deletarPermissao(id);
        await fetchPermissoes(); // Recarrega a lista
      } catch (deleteError) {
        console.error("Erro ao excluir permissão:", deleteError);
        alert("Não foi possível excluir a permissão.");
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
      <PermissoesTable
        permissoes={permissoes}
        onEdit={handleOpenModalForEdit}
        onDelete={handleDelete}
      />
    );
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Gerir Permissões</h1>
        <button
          onClick={handleOpenModalForAdd}
          className="px-4 py-2 bg-green-900 text-white font-semibold rounded-md shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Adicionar Permissão
        </button>
      </div>

      {renderContent()}

      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title={
          editingPermissao ? "Editar Permissão" : "Adicionar Nova Permissão"
        }
      >
        <PermissaoForm
          initialData={editingPermissao || {}}
          onSubmit={handleFormSubmit}
          onCancel={handleCloseModal}
          isSaving={isSaving}
        />
      </Modal>
    </div>
  );
}

export default PermissoesPage;
