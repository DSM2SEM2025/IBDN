import { Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import PrivateRoute from "./components/PrivateRoute";
import EmpresasPage from "./pages/EmpresasPage";
import RamosPage from "./pages/RamosPage";
import PermissoesPage from "./pages/PermissoesPage";
import PerfisPage from "./pages/PerfisPage";
import UsuariosPage from "./pages/UsuariosPage";
import SelosPage from "./pages/SelosPage";
import EmpresaDetailPage from "./pages/EmpresaDetailPage"; // 1. Importar a nova página

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

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

      {/* 2. Adicionar a nova rota de detalhes da empresa */}
      <Route
        path="/empresas/:empresaId"
        element={
          <PrivateRoute>
            <EmpresaDetailPage />
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
        path="/permissoes"
        element={
          <PrivateRoute>
            <PermissoesPage />
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
        path="/utilizadores"
        element={
          <PrivateRoute>
            <UsuariosPage />
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
    </Routes>
  );
}

export default App;
