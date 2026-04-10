import React, { useState } from "react";
import useAuthStore from "../store/authStore";
import { Link } from "react-router-dom";
import { Building, Sparkles, LayoutDashboard, X } from "lucide-react";
import CriarEmpresaPage from "./CriarEmpresaPage";

function HomePage() {
  const [showModal, setShowModal] = useState(false);
  const { user } = useAuthStore();

  const needsToCreateCompany =
    user && user.permissoes.includes("empresa") && !user.empresa_id;

  return (
    <div className="space-y-8 animate-fade-in-up">
      <div className="border-b border-gray-200 pb-5">
        <h1 className="text-4xl font-serif font-bold text-ibdn-primary tracking-tight">
          Sua Jornada Ambiental
        </h1>
        <p className="mt-2 text-lg text-gray-600 max-w-3xl">
          Bem-vindo ao Portal de Excelência em Governança Ambiental.
        </p>
      </div>

      {needsToCreateCompany ? (
        <div className="premium-glass bg-ibdn-accent/10 border-l-4 border-ibdn-accent p-8 rounded-2xl flex flex-col md:flex-row items-center gap-6">
          <div className="w-16 h-16 rounded-full bg-ibdn-accent/20 flex items-center justify-center shrink-0">
            <Building className="w-8 h-8 text-ibdn-earthy" strokeWidth={1.5} />
          </div>
          <div className="flex-1">
            <h2 className="font-serif font-bold text-2xl text-ibdn-earthy">
              Conclua o seu Perfil Corporativo
            </h2>
            <p className="mt-2 text-gray-700 text-lg leading-relaxed">
              O seu registro está quase completo. O próximo passo é registrar os
              dados da sua empresa para ter acesso a todas as funcionalidades de
              certificação e emissão de selos de impacto da plataforma.
            </p>
            <div className="mt-6 flex">
              <button
                onClick={() => setShowModal(true)}
                className="inline-flex items-center justify-center px-6 py-3 bg-ibdn-primary text-white font-medium rounded-xl shadow-lg shadow-ibdn-primary/20 hover:bg-ibdn-primary-focus hover:-translate-y-0.5 transition-all duration-200"
              >
                Configurar Empresa Agora
                <Sparkles className="w-4 h-4 ml-2" />
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="premium-card bg-white p-8 rounded-3xl shadow-sm border border-gray-100 flex flex-col justify-between items-start col-span-1 md:col-span-2">
            <div>
              <div className="w-12 h-12 rounded-full bg-ibdn-bg flex items-center justify-center mb-6">
                <LayoutDashboard className="w-6 h-6 text-ibdn-primary" strokeWidth={1.5} />
              </div>
              <h3 className="font-serif font-bold text-2xl text-gray-900 mb-3">Painel de Controle</h3>
              <p className="text-gray-600 text-lg leading-relaxed">
                Utilize o menu lateral para navegar pelas seções do sistema. Aqui você poderá acompanhar os processos de auditoria, visualizar o status dos seus selos ativos e gerenciar credenciais operacionais.
              </p>
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-ibdn-primary to-ibdn-primary-focus text-white p-8 rounded-3xl shadow-lg flex flex-col justify-center items-center text-center">
             <Sparkles className="w-12 h-12 text-ibdn-accent mb-4 opacity-80" strokeWidth={1} />
             <h4 className="font-medium text-lg text-white/90">Faça Parte</h4>
             <p className="mt-2 text-3xl font-serif font-bold">Liderança Verde</p>
             <p className="mt-4 text-sm text-white/70">O progresso corporativo transformado em impacto global e ação climática.</p>
          </div>
        </div>
      )}

      {/* Modal de Criação de Empresa */}
      {showModal && (
        <div className="fixed inset-0 bg-black/80 z-[100] flex items-center justify-center p-4 overflow-y-auto backdrop-blur-sm">
          <div className="relative w-full max-w-4xl max-h-[90vh] overflow-y-auto bg-ibdn-bg rounded-3xl shadow-2xl custom-scrollbar animate-fade-in-up">
            <button 
              onClick={() => setShowModal(false)}
              className="absolute top-4 right-4 p-2 bg-gray-100 hover:bg-gray-200 rounded-full text-gray-500 transition-colors z-10"
            >
              <X className="w-5 h-5" />
            </button>
            <div className="p-2">
              <CriarEmpresaPage asModal onClose={() => setShowModal(false)} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default HomePage;
