import React, { useState, useEffect } from "react";
import * as perfilService from "../services/perfilService";
import * as permissaoService from "../services/permissaoService"; // Precisamos das permissões
import PerfisTable from "../components/PerfisTable";
import Modal from "../components/Modal";
import PerfilForm from "../components/PerfilForm";
import AssociarPermissoes from "../components/AssociarPermissoes";

const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-10">
    <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-indigo-600"></div>
  </div>
);

function PerfisPage() {
  const [perfis, setPerfis] = useState([]);
  const [todasPermissoes, setTodasPermissoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Estados para gerir o modal
  const [modalState, setModalState] = useState({
    isOpen: false,
    mode: null,
    data: null,
  });
  const [isSaving, setIsSaving] = useState(false);

  // Função para carregar todos os dados necessários
  const fetchData = async () => {
    try {
      setLoading(true);
      // Busca perfis e todas as permissões em paralelo
      const [perfisData, permissoesData] = await Promise.all([
        perfilService.listarPerfis(),
        permissaoService.listarPermissoes(),
      ]);
      setPerfis(perfisData);
      setTodasPermissoes(permissoesData);
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
    setModalState({ isOpen: false, mode: null, data: null });
  };

  const handleOpenAddModal = () =>
    setModalState({ isOpen: true, mode: "ADD_EDIT_PERFIL", data: null });
  const handleOpenEditModal = (perfil) =>
    setModalState({ isOpen: true, mode: "ADD_EDIT_PERFIL", data: perfil });
  const handleOpenManagePermissionsModal = (perfil) =>
    setModalState({ isOpen: true, mode: "MANAGE_PERMISSIONS", data: perfil });

  // --- Funções de Submissão ---
  const handleProfileFormSubmit = async (formData) => {
    setIsSaving(true);
    try {
      if (modalState.data) {
        // Modo de Edição
        await perfilService.atualizarPerfil(modalState.data.id, formData);
      } else {
        // Modo de Criação
        await perfilService.criarPerfil(formData);
      }
      handleCloseModal();
      await fetchData();
    } catch (err) {
      alert("Não foi possível salvar o perfil.");
    } finally {
      setIsSaving(false);
    }
  };

  const handlePermissionsSubmit = async (novasPermissoesIds) => {
    setIsSaving(true);
    const perfilId = modalState.data.id;
    const permissoesAtuaisIds = new Set(
      modalState.data.permissoes.map((p) => p.id)
    );

    // Transforma o array de IDs em um Set para facilitar a comparação
    const novasPermissoesSet = new Set(novasPermissoesIds);

    try {
      // Permissões para adicionar: estão no novo set, mas não no antigo
      const paraAdicionar = novasPermissoesIds.filter(
        (id) => !permissoesAtuaisIds.has(id)
      );

      // Permissões para remover: estão no antigo set, mas não no novo
      const paraRemover = [...permissoesAtuaisIds].filter(
        (id) => !novasPermissoesSet.has(id)
      );

      // Executa as chamadas à API em paralelo
      await Promise.all([
        ...paraAdicionar.map((id) =>
          perfilService.adicionarPermissaoAoPerfil(perfilId, id)
        ),
        ...paraRemover.map((id) =>
          perfilService.removerPermissaoDoPerfil(perfilId, id)
        ),
      ]);

      handleCloseModal();
      await fetchData();
    } catch (err) {
      alert("Ocorreu um erro ao atualizar as permissões.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async (perfilId) => {
    if (window.confirm("Tem a certeza que deseja excluir este perfil?")) {
      try {
        await perfilService.deletarPerfil(perfilId);
        await fetchData();
      } catch (err) {
        alert("Não foi possível excluir o perfil.");
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
      <PerfisTable
        perfis={perfis}
        onEdit={handleOpenEditModal}
        onDelete={handleDelete}
        onManagePermissions={handleOpenManagePermissionsModal}
      />
    );
  };

  const getModalTitle = () => {
    if (modalState.mode === "ADD_EDIT_PERFIL")
      return modalState.data ? "Editar Perfil" : "Adicionar Novo Perfil";
    if (modalState.mode === "MANAGE_PERMISSIONS") return "Gerir Permissões";
    return "";
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Gerir Perfis</h1>
        <button
          onClick={handleOpenAddModal}
          className="px-4 py-2 bg-indigo-600 text-white font-semibold rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Adicionar Perfil
        </button>
      </div>

      {renderContent()}

      <Modal
        isOpen={modalState.isOpen}
        onClose={handleCloseModal}
        title={getModalTitle()}
      >
        {modalState.mode === "ADD_EDIT_PERFIL" && (
          <PerfilForm
            initialData={modalState.data || {}}
            onSubmit={handleProfileFormSubmit}
            onCancel={handleCloseModal}
            isSaving={isSaving}
          />
        )}
        {modalState.mode === "MANAGE_PERMISSIONS" && (
          <AssociarPermissoes
            perfil={modalState.data}
            todasPermissoes={todasPermissoes}
            onSave={handlePermissionsSubmit}
            onCancel={handleCloseModal}
            isSaving={isSaving}
          />
        )}
      </Modal>
    </div>
  );
}

export default PerfisPage;
