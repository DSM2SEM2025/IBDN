// front_e_back/src/pages/CriarEmpresaPage.jsx
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

function CriarEmpresaPage({ asModal, onClose }) {
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

  // Redireciona se o usuário já tiver uma empresa associada (somente se não for modal)
  if (user?.empresa_id && !asModal) {
    return <Navigate to="/" replace />;
  }

  const handleCancelClick = () => {
    if (onClose) onClose();
    else navigate("/");
  };

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

    // --- VALIDAÇÃO ADICIONADA AQUI ---
    // Verifica se o array de IDs de ramos está vazio ou não foi fornecido.
    if (!ramosIds || ramosIds.length === 0) {
      alert(
        "Você deve selecionar pelo menos um ramo de atividade para continuar."
      );
      setIsSaving(false); // Libera o botão
      return; // Interrompe a execução da função
    }

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
        "Empresa, endereço e ramos registrados com sucesso! Por favor, faça login novamente para atualizar seu perfil."
      );
      logout(); // Força o logout para o token ser atualizado com o novo empresa_id
      navigate("/login");
    } catch (error) {
      console.error("Erro completo ao finalizar registro:", error); // Log para depuração
      alert(
        error.response?.data?.detail ||
          "Ocorreu um erro ao finalizar o registro."
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
          <div className="animate-fade-in-up">
            <h2 className="text-2xl font-serif font-bold text-ibdn-primary mb-6">
              Dados Fundamentais da Empresa
            </h2>
            <EmpresaForm
              onSubmit={handleNextFromEmpresa}
              onCancel={handleCancelClick}
            />
          </div>
        );
      case 2:
        return (
          <div className="animate-fade-in-up">
            <h2 className="text-2xl font-serif font-bold text-ibdn-primary mb-6">
              Localização Sede
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
          <div className="animate-fade-in-up">
            <h2 className="text-2xl font-serif font-bold text-ibdn-primary mb-6">
              Área de Impacto e Atuação
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

  const steps = [
    { title: "Identificação", number: 1 },
    { title: "Localização", number: 2 },
    { title: "Impacto e Ramo", number: 3 },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-serif font-bold text-ibdn-primary">
          Formalize seu Impacto
        </h1>
        <p className="text-gray-600 mt-3 text-lg max-w-2xl mx-auto">
          Inicie sua certificação preenchendo os dados corporativos. Cuidamos das informações com segurança.
        </p>
      </div>

      <div className="flex justify-center mb-10 relative">
        {/* Timeline Progress */}
        <div className="absolute top-1/2 left-0 w-full h-1 bg-gray-200 -z-10 rounded-full transform -translate-y-1/2 px-16">
          <div 
            className="h-full bg-ibdn-accent transition-all duration-500 ease-in-out rounded-full" 
            style={{ width: `${((etapa - 1) / (steps.length - 1)) * 100}%` }}
          />
        </div>
        
        <div className="flex justify-between w-full max-w-2xl px-4">
          {steps.map((step) => {
            const isCompleted = etapa > step.number;
            const isCurrent = etapa === step.number;
            
            return (
              <div key={step.number} className="flex flex-col items-center">
                <div 
                  className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg mb-2 shadow-sm transition-all duration-300 ${
                    isCurrent 
                      ? 'bg-ibdn-primary text-ibdn-accent ring-4 ring-ibdn-primary/20 scale-110' 
                      : isCompleted 
                        ? 'bg-ibdn-accent text-ibdn-primary'
                        : 'bg-white text-gray-400 border-2 border-gray-200'
                  }`}
                >
                  {isCompleted ? '✓' : step.number}
                </div>
                <span className={`text-sm font-medium ${
                  isCurrent ? 'text-ibdn-primary' : 'text-gray-500'
                }`}>
                  {step.title}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      <div className="premium-card bg-white p-10 rounded-3xl shadow-lg border border-gray-100">
        {renderEtapa()}
      </div>
    </div>
  );
}

export default CriarEmpresaPage;
