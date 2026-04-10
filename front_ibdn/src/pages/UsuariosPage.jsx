import React, { useState, useEffect } from "react";
import * as usuarioService from "../services/usuarioService";
import * as perfilService from "../services/perfilService"; // Precisamos dos perfis para o formulário
import UsuariosTable from "../components/UsuariosTable";
import Modal from "../components/Modal";
import UsuarioForm from "../components/UsuarioForm";

const LoadingSpinner = () => (
  <div className="flex flex-col justify-center items-center p-20 premium-card bg-white rounded-3xl shadow-sm border border-gray-100 my-8">
    <div className="w-12 h-12 border-4 border-ibdn-primary/20 border-t-ibdn-primary rounded-full animate-spin mb-4"></div>
    <p className="text-ibdn-primary font-medium opacity-80">Carregando dados...</p>
  </div>
);

function UsuariosPage() {
  const [usuarios, setUsuarios] = useState([]);
  const [perfis, setPerfis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Estados para gerir o modal
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingUsuario, setEditingUsuario] = useState(null);
  const [isSaving, setIsSaving] = useState(false);

  // Função para carregar todos os dados necessários
  const fetchData = async () => {
    try {
      setLoading(true);
      // Busca utilizadores e perfis em paralelo para melhor performance
      const [usuariosData, perfisData] = await Promise.all([
        usuarioService.listarUsuarios(),
        perfilService.listarPerfis(),
      ]);
      setUsuarios(usuariosData);
      setPerfis(perfisData);
      setError(null);
    } catch (err) {
      setError("Falha ao carregar os dados. Tente novamente mais tarde.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // --- Funções para gerir o Modal ---
  const handleCloseModal = () => {
    if (isSaving) return;
    setIsModalOpen(false);
    setEditingUsuario(null);
  };

  const handleOpenAddModal = () => {
    setEditingUsuario(null);
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (usuario) => {
    setEditingUsuario(usuario);
    setIsModalOpen(true);
  };

  // --- Funções de Submissão e Exclusão ---
  const handleFormSubmit = async (formData) => {
    setIsSaving(true);
    try {
      if (editingUsuario) {
        // Modo de Edição
        await usuarioService.atualizarUsuario(editingUsuario.id, formData);
      } else {
        // Modo de Criação
        await usuarioService.criarUsuario(formData);
      }
      handleCloseModal();
      await fetchData();
    } catch (err) {
      alert("Não foi possível salvar o utilizador.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async (usuarioId) => {
    if (window.confirm("Tem a certeza que deseja excluir este utilizador?")) {
      try {
        await usuarioService.deletarUsuario(usuarioId);
        await fetchData();
      } catch (err) {
        alert("Não foi possível excluir o utilizador.");
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
      <UsuariosTable
        usuarios={usuarios}
        onEdit={handleOpenEditModal}
        onDelete={handleDelete}
      />
    );
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Gerir Utilizadores</h1>
        <button
          onClick={handleOpenAddModal}
          className="px-4 py-2 bg-green-900 text-white font-semibold rounded-md shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Adicionar Utilizador
        </button>
      </div>

      {renderContent()}

      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title={
          editingUsuario ? "Editar Utilizador" : "Adicionar Novo Utilizador"
        }
      >
        <UsuarioForm
          initialData={editingUsuario || {}}
          perfis={perfis}
          onSubmit={handleFormSubmit}
          onCancel={handleCloseModal}
          isSaving={isSaving}
        />
      </Modal>
    </div>
  );
}

export default UsuariosPage;
