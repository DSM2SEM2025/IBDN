// src/App.jsx
import { Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import PrivateRoute from "./components/PrivateRoute";
import EmpresasPage from "./pages/EmpresasPage";
import EmpresaDetailPage from "./pages/EmpresaDetailPage";
import RamosPage from "./pages/RamosPage";
import PermissoesPage from "./pages/PermissoesPage";
import PerfisPage from "./pages/PerfisPage";
import UsuariosPage from "./pages/UsuariosPage";
import SelosPage from "./pages/SelosPage";
import TiposSeloPage from "./pages/TiposSeloPage";
// NEW: Import the solicitations page
import SolicitacoesSeloPage from "./pages/SolicitacoesSeloPage";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      {/* Protected Routes */}
      <Route
        path="/"
        element={
          <PrivateRoute>
            <HomePage />
          </PrivateRoute>
        }
      />
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

      {/* NEW: Add the route for the new page */}
      <Route
        path="/solicitacoes-selo"
        element={
          <PrivateRoute>
            <SolicitacoesSeloPage />
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
