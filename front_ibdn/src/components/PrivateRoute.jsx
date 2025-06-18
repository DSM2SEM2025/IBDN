import React from "react";
import { Navigate } from "react-router-dom";
import useAuthStore from "../store/authStore";
import Layout from "./Layout";

// Este componente verifica se o utilizador está autenticado.
// Se estiver, renderiza a página solicitada dentro do Layout.
// Se não, redireciona para a página de login.
function PrivateRoute({ children }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  if (!isAuthenticated) {
    // Utilizador não autenticado, redireciona para a página de login
    return <Navigate to="/login" replace />;
  }

  // Utilizador autenticado, renderiza o layout com o conteúdo da página
  return <Layout>{children}</Layout>;
}

export default PrivateRoute;
