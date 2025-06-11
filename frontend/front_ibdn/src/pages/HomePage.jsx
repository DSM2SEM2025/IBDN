import React from "react";

function HomePage() {
  return (
    // O Layout já fornece o padding, então não precisamos de margens aqui.
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-4">
        Bem-vindo ao seu Painel!
      </h1>
      <div className="bg-white p-6 rounded-lg shadow">
        <p className="text-gray-700">
          Este é o seu painel de controlo principal. Use o menu à esquerda para
          navegar pelas diferentes secções da aplicação, como a gestão de
          empresas.
        </p>
      </div>
    </div>
  );
}

export default HomePage;
