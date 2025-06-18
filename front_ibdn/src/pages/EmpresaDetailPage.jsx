// front_e_back/front/src/pages/EmpresaDetailPage.jsx
import React, { useState, useEffect, useCallback } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";
import * as empresaService from "../services/empresaService";
import * as enderecoService from "../services/enderecoService";
import * as ramoService from "../services/ramoService";
import * as empresaRamoService from "../services/empresaRamoService";
import * as seloService from "../services/seloService";
import * as notificacaoService from "../services/notificacaoService";

import Modal from "../components/Modal";
import EnderecoForm from "../components/EnderecoForm";
import SelosAssociadosTable from "../components/SelosAssociadosTable";
import AssociarRamosForm from "../components/AssociarRamosForm";
import NotificacaoForm from "../components/NotificacaoForm";
import NotificacoesList from "../components/NotificacoesList";

const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-10">
    <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-indigo-600"></div>
  </div>
);

function EmpresaDetailPage() {
  const { empresaId } = useParams();
  const { user } = useAuthStore();
  const navigate = useNavigate();

  const isAdmin =
    user?.permissoes.includes("admin") ||
    user?.permissoes.includes("admin_master");

  useEffect(() => {
    if (user) {
      const isOwner = user.empresa_id?.toString() === empresaId;
      if (!isOwner && !isAdmin) {
        navigate("/");
      }
    }
  }, [empresaId, user, navigate, isAdmin]);

  const [empresa, setEmpresa] = useState(null);
  const [endereco, setEndereco] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [ramosAtuais, setRamosAtuais] = useState([]);
  const [todosOsRamos, setTodosOsRamos] = useState([]);
  const [selos, setSelos] = useState([]);
  const [notificacoes, setNotificacoes] = useState([]);

  const [modalState, setModalState] = useState({
    isOpen: false,
    mode: null,
    data: null,
  });
  const [isSaving, setIsSaving] = useState(false);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      const promises = [
        empresaService.buscarEmpresaPorId(empresaId),
        enderecoService.getEndereco(empresaId),
        empresaRamoService.getRamosPorEmpresa(empresaId),
        ramoService.listarRamos(),
        seloService.getSelosByEmpresa(empresaId),
      ];

      // Apenas admins buscam o histórico de notificações nesta tela
      if (isAdmin) {
        promises.push(notificacaoService.listarNotificacoesEmpresa(empresaId));
      }

      const [
        empresaData,
        enderecoData,
        ramosAtuaisData,
        todosOsRamosData,
        selosData,
        notificacoesData,
      ] = await Promise.all(promises);

      setEmpresa(empresaData);
      setEndereco(enderecoData);
      setRamosAtuais(ramosAtuaisData);
      setTodosOsRamos(todosOsRamosData);
      setSelos(selosData);
      if (notificacoesData) {
        setNotificacoes(notificacoesData);
      }
      setError(null);
    } catch (err) {
      if (err.response && err.response.status !== 404) {
        setError("Falha ao carregar os dados da empresa.");
      }
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [empresaId, isAdmin]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleCloseModal = () =>
    !isSaving && setModalState({ isOpen: false, mode: null, data: null });
  const handleOpenModal = (mode, data = null) =>
    setModalState({ isOpen: true, mode, data });

  const handleEnderecoSubmit = async (formData) => {
    setIsSaving(true);
    try {
      if (endereco) {
        await enderecoService.atualizarEndereco(empresaId, formData);
      } else {
        await enderecoService.criarEndereco(empresaId, formData);
      }
      handleCloseModal();
      await fetchData();
    } catch (err) {
      alert(
        err.response?.data?.detail || "Ocorreu um erro ao salvar o endereço."
      );
    } finally {
      setIsSaving(false);
    }
  };

  const handleRamosSubmit = async (selectedRamosIds) => {
    setIsSaving(true);
    try {
      await empresaRamoService.atrelarRamosAEmpresa(
        empresaId,
        selectedRamosIds
      );
      handleCloseModal();
      await fetchData();
    } catch (err) {
      alert("Erro ao atualizar os ramos de atividade.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleNotificacaoSubmit = async (formData) => {
    setIsSaving(true);
    try {
      await notificacaoService.criarNotificacao(empresaId, formData);
      handleCloseModal();
      await fetchData();
      alert("Notificação enviada com sucesso!");
    } catch (err) {
      alert("Erro ao enviar notificação.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleNotificacaoDelete = async (id) => {
    if (window.confirm("Tem certeza que deseja apagar esta notificação?")) {
      try {
        await notificacaoService.deletarNotificacao(id);
        await fetchData();
      } catch (err) {
        alert("Erro ao apagar notificação.");
      }
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error)
    return (
      <div className="text-center p-10 bg-red-100 text-red-700">{error}</div>
    );
  if (!empresa)
    return <div className="text-center p-10">Empresa não encontrada.</div>;

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

      {/* Seções de Dados, Endereço, Ramos e Selos (sem alteração) */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold text-gray-800 border-b pb-3 mb-4">
          Detalhes da Empresa: {empresa.razao_social}
        </h2>
        <p>
          <strong>CNPJ:</strong> {empresa.cnpj}
        </p>
        <p>
          <strong>Responsável:</strong> {empresa.responsavel || "N/A"}
        </p>
      </div>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex justify-between items-center border-b pb-3 mb-4">
          <h2 className="text-xl font-semibold text-gray-800">Endereço</h2>
          <button
            onClick={() => handleOpenModal("ENDERECO", endereco)}
            className="px-4 py-2 text-sm bg-green-900 text-white font-semibold rounded-md shadow-sm hover:bg-green-700"
          >
            {endereco ? "Editar Endereço" : "Adicionar Endereço"}
          </button>
        </div>
        {endereco ? (
          <div className="text-sm">
            <p>{`${endereco.logradouro}, ${endereco.numero} - ${endereco.bairro}`}</p>
            <p>{`${endereco.cidade} - ${endereco.uf}, CEP: ${endereco.cep}`}</p>
            {endereco.complemento && <p>Complemento: {endereco.complemento}</p>}
          </div>
        ) : (
          <p className="text-sm text-gray-500">Nenhum endereço registrado.</p>
        )}
      </div>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex justify-between items-center border-b pb-3 mb-4">
          <h2 className="text-xl font-semibold text-gray-800">
            Ramos de Atividade
          </h2>
          <button
            onClick={() => handleOpenModal("RAMOS")}
            className="px-4 py-2 text-sm bg-green-900 text-white font-semibold rounded-md shadow-sm hover:bg-green-700"
          >
            Gerenciar
          </button>
        </div>
        {ramosAtuais.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {ramosAtuais.map((ramo) => (
              <span
                key={ramo.id}
                className="bg-gray-200 text-gray-800 text-xs font-semibold mr-2 px-2.5 py-0.5 rounded-full"
              >
                {ramo.nome}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-sm text-gray-500">
            Nenhum ramo de atividade associado.
          </p>
        )}
      </div>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold text-gray-800 border-b pb-3 mb-4">
          Selos da Empresa
        </h2>
        <SelosAssociadosTable selos={selos} />
      </div>

      {/* SEÇÃO DE NOTIFICAÇÕES (VISÍVEL APENAS PARA ADMINS) */}
      {isAdmin && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex justify-between items-center border-b pb-3 mb-4">
            <h2 className="text-xl font-semibold text-gray-800">
              Notificações da Empresa
            </h2>
            <button
              onClick={() => handleOpenModal("NOTIFICACAO")}
              className="px-4 py-2 text-sm bg-green-600 text-white font-semibold rounded-md shadow-sm hover:bg-green-700"
            >
              Enviar Notificação
            </button>
          </div>
          <NotificacoesList
            notificacoes={notificacoes}
            onDelete={handleNotificacaoDelete}
            isAdminView={true}
          />
        </div>
      )}

      {/* MODAIS */}
      <Modal
        isOpen={modalState.isOpen}
        onClose={handleCloseModal}
        title={
          modalState.mode === "ENDERECO"
            ? endereco
              ? "Editar Endereço"
              : "Adicionar Endereço"
            : `Gerenciar ${modalState.mode}`
        }
      >
        {modalState.mode === "ENDERECO" && (
          <EnderecoForm
            formData={modalState.data || {}}
            setFormData={(updater) =>
              setModalState((s) => ({
                ...s,
                data: typeof updater === "function" ? updater(s.data) : updater,
              }))
            }
            onSubmit={handleEnderecoFormSubmit}
            onCancel={handleCloseModal}
            isSaving={isSaving}
          />
        )}
        {modalState.mode === "RAMOS" && (
          <AssociarRamosForm
            ramosAtuais={ramosAtuais}
            todosOsRamos={todosOsRamos}
            onSave={handleRamosSubmit}
            onCancel={handleCloseModal}
            isSaving={isSaving}
          />
        )}
        {modalState.mode === "NOTIFICACAO" && (
          <NotificacaoForm
            onSubmit={handleNotificacaoSubmit}
            onCancel={handleCloseModal}
            isSaving={isSaving}
          />
        )}
      </Modal>
    </div>
  );
}

export default EmpresaDetailPage;
