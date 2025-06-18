// front_e_back/src/pages/CriarEmpresaPage.jsx
import React, { useState, useEffect } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import useAuthStore from "../store/authStore";
import * as empresaService from "../services/empresaService";
import * as enderecoService from "../services/enderecoService";
import * as ramoService from "../services/ramoService";
import * as empresaRamoService from "../services/empresaRamoService";

import EmpresaForm from "../components/EmpresaForm";
import EnderecoForm from "../components/EnderecoForm";
import AssociarRamosForm from "../components/AssociarRamosForm";

function CriarEmpresaPage() {
  const [etapa, setEtapa] = useState(1);

  // Estado para cada parte do formulário
  const [dadosEmpresa, setDadosEmpresa] = useState(null);
  const [dadosEndereco, setDadosEndereco] = useState({
    cep: "",
    logradouro: "",
    numero: "",
    complemento: "",
    bairro: "",
    cidade: "",
    uf: "",
  });

  const [todosOsRamos, setTodosOsRamos] = useState([]);
  const [isSaving, setIsSaving] = useState(false);
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  useEffect(() => {
    ramoService.listarRamos().then(setTodosOsRamos).catch(console.error);
  }, []);

  // Redireciona se o usuário já tiver uma empresa associada
  if (user?.empresa_id) {
    return <Navigate to="/" replace />;
  }

  const handleNextFromEmpresa = (data) => {
    setDadosEmpresa(data);
    setEtapa(2);
  };

  const handleNextFromEndereco = (data) => {
    setDadosEndereco(data);
    setEtapa(3);
  };

  const handleFinalSubmit = async (ramosIds) => {
    setIsSaving(true);
    if (!dadosEmpresa || !dadosEndereco) {
      alert("Dados da empresa ou endereço estão em falta.");
      setIsSaving(false);
      return;
    }

    try {
      const novaEmpresa = await empresaService.adicionarEmpresa(dadosEmpresa);
      const novaEmpresaId = novaEmpresa.id;

      // Chama o serviço para criar o endereço, passando o ID da nova empresa
      await enderecoService.criarEndereco(novaEmpresaId, dadosEndereco);
      // Chama o serviço para atrelar os ramos à empresa
      await empresaRamoService.atrelarRamosAEmpresa(novaEmpresaId, ramosIds);

      alert(
        "Empresa, endereço e ramos registados com sucesso! Por favor, faça login novamente para atualizar o seu perfil."
      );
      logout(); // Força o logout para o token ser atualizado com o novo empresa_id
      navigate("/login");
    } catch (error) {
      console.error("Erro completo ao finalizar registro:", error); // Log para depuração
      alert(
        error.response?.data?.detail ||
          "Ocorreu um erro ao finalizar o registo."
      );
      // Volta para a primeira etapa em caso de erro para permitir correção
      setEtapa(1);
    } finally {
      setIsSaving(false);
    }
  };

  const renderEtapa = () => {
    switch (etapa) {
      case 1:
        return (
          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              Etapa 1 de 3: Dados da Empresa
            </h2>
            <EmpresaForm
              onSubmit={handleNextFromEmpresa}
              onCancel={() => navigate("/")}
            />
          </div>
        );
      case 2:
        return (
          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              Etapa 2 de 3: Endereço
            </h2>
            <EnderecoForm
              formData={dadosEndereco}
              setFormData={setDadosEndereco}
              onSubmit={handleNextFromEndereco}
              onCancel={() => setEtapa(1)}
            />
          </div>
        );
      case 3:
        return (
          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              Etapa 3 de 3: Ramo de Atividade
            </h2>
            <AssociarRamosForm
              ramosAtuais={[]} // No momento da criação, a empresa não tem ramos associados ainda
              todosOsRamos={todosOsRamos}
              onSave={handleFinalSubmit}
              onCancel={() => setEtapa(2)}
              isSaving={isSaving}
            />
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-lg max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Registo da Empresa</h1>
        <p className="text-gray-600 mt-2">
          Siga os passos para completar o seu perfil.
        </p>
      </div>
      {renderEtapa()}
    </div>
  );
}

export default CriarEmpresaPage;
