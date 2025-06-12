import { Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import PrivateRoute from "./components/PrivateRoute";
import EmpresasPage from "./pages/EmpresasPage"; // 1. Importar a nova página

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

      {/* 2. Adicionar a nova rota protegida para a página de empresas */}
      <Route
        path="/empresas"
        element={
          <PrivateRoute>
            <EmpresasPage />
          </PrivateRoute>
        }
      />
    </Routes>
  );
}

export default App;
