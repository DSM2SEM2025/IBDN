import React from "react";
import useAuthStore from "../store/authStore";
import { Link } from "react-router-dom";

function HomePage() {
  const { user } = useAuthStore();

  // Verifica se o utilizador tem a permissão 'empresa' mas ainda não tem um 'empresa_id'
  const needsToCreateCompany =
    user && user.permissoes.includes("empresa") && !user.empresa_id;

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-4">
        Bem-vindo ao seu Painel!
      </h1>

      {needsToCreateCompany ? (
        <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-6 rounded-lg shadow-lg">
          <h2 className="font-bold text-xl">Ação Requerida</h2>
          <p className="mt-2">
            O seu registro está quase completo. O próximo passo é Registrar os
            dados da sua empresa para ter acesso a todas as funcionalidades da
            plataforma.
          </p>
          <Link
            to="/criar-empresa"
            className="mt-4 inline-block px-6 py-2 bg-yellow-500 text-white font-semibold rounded-md shadow-sm hover:bg-yellow-600"
          >
            Registrar Empresa Agora
          </Link>
        </div>
      ) : (
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-gray-700">
            Use o menu à esquerda para navegar pelas diferentes secções da
            aplicação.
          </p>
        </div>
      )}
    </div>
  );
}

export default HomePage;
