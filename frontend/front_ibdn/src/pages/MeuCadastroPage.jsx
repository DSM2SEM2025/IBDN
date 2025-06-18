import React, { useState, useEffect, useCallback } from "react";
import useAuthStore from "../store/authStore";
import * as empresaService from "../services/empresaService";
import * as enderecoService from "../services/enderecoService";
import * as ramoService from "../services/ramoService";
import * as empresaRamoService from "../services/empresaRamoService";
import * as seloService from "../services/seloService";

import Modal from "../components/Modal";
import EmpresaForm from "../components/EmpresaForm";
import EnderecoForm from "../components/EnderecoForm";
import AssociarRamosForm from "../components/AssociarRamosForm";
import SelosAssociadosTable from "../components/SelosAssociadosTable";

const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-10">
    <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-indigo-600"></div>
  </div>
);

function MeuCadastroPage() {
  const { user } = useAuthStore();
  const empresaId = user?.empresa_id;

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Estados para os dados da página
  const [empresa, setEmpresa] = useState(null);
  const [endereco, setEndereco] = useState(null);
  const [ramosAtuais, setRamosAtuais] = useState([]);
  const [todosOsRamos, setTodosOsRamos] = useState([]);
  const [selos, setSelos] = useState([]);

  // Estados para controle dos modais
  const [modalState, setModalState] = useState({ isOpen: false, mode: null });
  const [isSaving, setIsSaving] = useState(false);

  const fetchData = useCallback(async () => {
    if (!empresaId) {
      setError("Usuário não associado a uma empresa.");
      setLoading(false);
      return;
    }
    try {
      setLoading(true);
      const [
        empresaData,
        enderecoData,
        ramosAtuaisData,
        todosOsRamosData,
        selosData,
      ] = await Promise.all([
        empresaService.buscarEmpresaPorId(empresaId),
        enderecoService.getEndereco(empresaId),
        empresaRamoService.getRamosPorEmpresa(empresaId),
        ramoService.listarRamos(),
        seloService.getSelosByEmpresa(empresaId),
      ]);

      setEmpresa(empresaData);
      setEndereco(enderecoData);
      setRamosAtuais(ramosAtuaisData);
      setTodosOsRamos(todosOsRamosData);
      setSelos(selosData);
      setError(null);
    } catch (err) {
      setError("Falha ao carregar os dados do seu cadastro.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [empresaId]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleCloseModal = () =>
    !isSaving && setModalState({ isOpen: false, mode: null });

  const handleEditEmpresa = async (formData) => {
    setIsSaving(true);
    try {
      await empresaService.atualizarEmpresa(empresaId, formData);
      handleCloseModal();
      await fetchData();
    } catch (err) {
      alert("Erro ao atualizar os dados da empresa.");
    } finally {
      setIsSaving(false);
    }
  };

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
      alert("Erro ao salvar o endereço.");
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

  if (loading) return <LoadingSpinner />;
  if (error)
    return (
      <div className="text-center p-10 bg-red-100 text-red-700">{error}</div>
    );

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold text-gray-900">Meu Cadastro</h1>

      {/* Seção Dados da Empresa */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex justify-between items-center border-b pb-3 mb-4">
          <h2 className="text-xl font-semibold text-gray-800">
            Dados da Empresa
          </h2>
          <button
            onClick={() => setModalState({ isOpen: true, mode: "EMPRESA" })}
            className="px-4 py-2 text-sm bg-indigo-600 text-white font-semibold rounded-md shadow-sm hover:bg-indigo-700"
          >
            Editar
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <p>
            <strong>Razão Social:</strong> {empresa?.razao_social}
          </p>
          <p>
            <strong>Nome Fantasia:</strong> {empresa?.nome_fantasia || "N/A"}
          </p>
          <p>
            <strong>CNPJ:</strong> {empresa?.cnpj}
          </p>
          <p>
            <strong>Responsável:</strong> {empresa?.responsavel || "N/A"}
          </p>
          <p>
            <strong>Telefone:</strong> {empresa?.telefone || "N/A"}
          </p>
          <p>
            <strong>Site:</strong> {empresa?.site || "N/A"}
          </p>
          <p>
            <strong>Cargo Responsavel:</strong>{" "}
            {empresa?.cargo_responsavel || "N/A"}
          </p>
        </div>
      </div>

      {/* Seção Endereço */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex justify-between items-center border-b pb-3 mb-4">
          <h2 className="text-xl font-semibold text-gray-800">Endereço</h2>
          <button
            onClick={() => setModalState({ isOpen: true, mode: "ENDERECO" })}
            className="px-4 py-2 text-sm bg-indigo-600 text-white font-semibold rounded-md shadow-sm hover:bg-indigo-700"
          >
            {endereco ? "Editar" : "Adicionar"}
          </button>
        </div>
        {endereco ? (
          <div className="text-sm">
            <p>{`${endereco.logradouro}, ${endereco.numero} - ${endereco.bairro}`}</p>
            <p>{`${endereco.cidade} - ${endereco.uf}, CEP: ${endereco.cep}`}</p>
            {endereco.complemento && <p>Complemento: {endereco.complemento}</p>}
          </div>
        ) : (
          <p className="text-sm text-gray-500">Nenhum endereço cadastrado.</p>
        )}
      </div>

      {/* Seção Ramos */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex justify-between items-center border-b pb-3 mb-4">
          <h2 className="text-xl font-semibold text-gray-800">
            Ramos de Atividade
          </h2>
          <button
            onClick={() => setModalState({ isOpen: true, mode: "RAMOS" })}
            className="px-4 py-2 text-sm bg-indigo-600 text-white font-semibold rounded-md shadow-sm hover:bg-indigo-700"
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

      {/* Seção Selos */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold text-gray-800 border-b pb-3 mb-4">
          Meus Selos
        </h2>
        <SelosAssociadosTable selos={selos} />
      </div>

      {/* Modais */}
      <Modal
        isOpen={modalState.isOpen}
        onClose={handleCloseModal}
        title={`Editar ${modalState.mode}`}
      >
        {modalState.mode === "EMPRESA" && (
          <EmpresaForm
            initialData={empresa}
            onSubmit={handleEditEmpresa}
            onCancel={handleCloseModal}
            isSaving={isSaving}
          />
        )}
        {modalState.mode === "ENDERECO" && (
          <EnderecoForm
            formData={endereco || {}}
            setFormData={setEndereco}
            onSubmit={handleEnderecoSubmit}
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
      </Modal>
    </div>
  );
}

export default MeuCadastroPage;
