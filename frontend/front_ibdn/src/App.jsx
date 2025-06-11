import { Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import PrivateRoute from "./components/PrivateRoute"; // 1. Importar o PrivateRoute

function App() {
  return (
    <Routes>
      {/* Rota pública para a página de login */}
      <Route path="/login" element={<LoginPage />} />

      {/* Rota raiz protegida */}
      {/* Envolvemos a HomePage com o PrivateRoute */}
      <Route
        path="/"
        element={
          <PrivateRoute>
            <HomePage />
          </PrivateRoute>
        }
      />

      {/* Exemplo de como adicionar outra rota protegida no futuro */}
      {/* <Route
        path="/empresas"
        element={
          <PrivateRoute>
            <EmpresasPage />
          </PrivateRoute>
        }
      />
      */}
    </Routes>
  );
}

export default App;
