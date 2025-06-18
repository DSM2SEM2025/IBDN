// front_e_back/src/pages/EmpresaDetailPage.jsx
import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import * as empresaService from "../services/empresaService";
import * as enderecoService from "../services/enderecoService";
import EnderecosTable from "../components/EnderecosTable";
import EnderecoForm from "../components/EnderecoForm";
import Modal from "../components/Modal";
// ... outros imports

const LoadingSpinner = () => (
  <div className="flex justify-center items-center p-10">
    <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-indigo-600"></div>
  </div>
);

function EmpresaDetailPage() {
  const { empresaId } = useParams();
  const [empresa, setEmpresa] = useState(null);
  const [endereco, setEndereco] = useState(null); // Estado para um único endereço
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [modalState, setModalState] = useState({
    isOpen: false,
    mode: null,
    data: null,
  });
  const [isSaving, setIsSaving] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [empresaData, enderecoData] = await Promise.all([
        empresaService.buscarEmpresaPorId(empresaId),
        enderecoService.getEndereco(empresaId), // Usamos o serviço que busca um único endereço
      ]);
      setEmpresa(empresaData);
      setEndereco(enderecoData);
      setError(null);
    } catch (err) {
      if (err.response && err.response.status !== 404) {
        setError("Falha ao carregar os dados da empresa.");
      }
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [empresaId]);

  const handleCloseModal = () =>
    !isSaving && setModalState({ isOpen: false, mode: null, data: null });

  const handleOpenEnderecoModal = () => {
    // Passa o endereço existente (ou null) para o modal
    setModalState({ isOpen: true, mode: "ADD_EDIT_ENDERECO", data: endereco });
  };

  const handleEnderecoFormSubmit = async (formData) => {
    setIsSaving(true);
    try {
      // Se já existe um endereço (modalState.data não é nulo), atualiza. Senão, cria.
      if (modalState.data) {
        await enderecoService.atualizarEndereco(empresaId, formData);
      } else {
        await enderecoService.criarEndereco(empresaId, formData);
      }
      handleCloseModal();
      await fetchData();
    } catch (err) {
      alert(err.detail || "Ocorreu um erro ao salvar o endereço.");
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
      <div>
        <Link
          to="/empresas"
          className="text-sm font-medium text-indigo-600 hover:text-indigo-800"
        >
          &larr; Voltar para a lista de empresas
        </Link>
      </div>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold text-gray-800 border-b pb-3 mb-4">
          Detalhes da Empresa
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
            onClick={handleOpenEnderecoModal}
            className="px-4 py-2 text-sm bg-indigo-600 text-white font-semibold rounded-md shadow-sm hover:bg-indigo-700"
          >
            {endereco ? "Editar Endereço" : "Adicionar Endereço"}
          </button>
        </div>
        {endereco ? (
          <EnderecosTable
            enderecos={[endereco]}
            onEdit={handleOpenEnderecoModal}
          />
        ) : (
          <p className="text-sm text-gray-500">Nenhum endereço registado.</p>
        )}
      </div>

      {/* Adicionar aqui as secções para Ramos e Selos no futuro */}

      <Modal
        isOpen={modalState.isOpen}
        onClose={handleCloseModal}
        title={endereco ? "Editar Endereço" : "Adicionar Endereço"}
      >
        {modalState.mode === "ADD_EDIT_ENDERECO" && (
          <EnderecoForm
            formData={
              modalState.data || {
                cep: "",
                logradouro: "",
                numero: "",
                complemento: "",
                bairro: "",
                cidade: "",
                uf: "",
              }
            }
            setFormData={(data) => setModalState((prev) => ({ ...prev, data }))}
            onSubmit={handleEnderecoFormSubmit}
            onCancel={handleCloseModal}
            isSaving={isSaving}
          />
        )}
      </Modal>
    </div>
  );
}

export default EmpresaDetailPage;
