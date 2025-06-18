// src/App.jsx
import { Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import PrivateRoute from "./components/PrivateRoute";
import EmpresasPage from "./pages/EmpresasPage";
import EmpresaDetailPage from "./pages/EmpresaDetailPage";
import CriarEmpresaPage from "./pages/CriarEmpresaPage";
import RamosPage from "./pages/RamosPage";
import PermissoesPage from "./pages/PermissoesPage";
import PerfisPage from "./pages/PerfisPage";
import UsuariosPage from "./pages/UsuariosPage";
import SelosPage from "./pages/SelosPage";
import TiposSeloPage from "./pages/TiposSeloPage";
import SolicitacoesSeloPage from "./pages/SolicitacoesSeloPage";
import SolicitarSeloPage from "./pages/SolicitarSeloPage";
import MeuCadastroPage from "./pages/MeuCadastroPage"; // 1. Importar a nova página

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Rota para a página de criação de empresa em etapas */}
      <Route
        path="/criar-empresa"
        element={
          <PrivateRoute>
            <CriarEmpresaPage />
          </PrivateRoute>
        }
      />
      {/* 2. Adicionar a nova rota */}
      <Route
        path="/meu-cadastro"
        element={
          <PrivateRoute>
            <MeuCadastroPage />
          </PrivateRoute>
        }
      />

      {/* Rotas Protegidas que exigem autenticação */}
      <Route
        path="/"
        element={
          <PrivateRoute>
            <HomePage />
          </PrivateRoute>
        }
      />

      {/* ...demais rotas... */}
      <Route
        path="/empresas"
        element={
          <PrivateRoute>
            <EmpresasPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/empresas/:empresaId"
        element={
          <PrivateRoute>
            <EmpresaDetailPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/tipos-selo"
        element={
          <PrivateRoute>
            <TiposSeloPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/solicitacoes-selo"
        element={
          <PrivateRoute>
            <SolicitacoesSeloPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/solicitar-selo"
        element={
          <PrivateRoute>
            <SolicitarSeloPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/selos"
        element={
          <PrivateRoute>
            <SelosPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/ramos"
        element={
          <PrivateRoute>
            <RamosPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/utilizadores"
        element={
          <PrivateRoute>
            <UsuariosPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/perfis"
        element={
          <PrivateRoute>
            <PerfisPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/permissoes"
        element={
          <PrivateRoute>
            <PermissoesPage />
          </PrivateRoute>
        }
      />
    </Routes>
  );
}

export default App;
