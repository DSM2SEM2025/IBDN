import React, { useState } from "react";
// 1. Importar o Link
import { useNavigate, Link } from "react-router-dom";
import { login as authServiceLogin } from "../services/authService";
import useAuthStore from "../store/authStore";

function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const loginToStore = useAuthStore((state) => state.login);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    try {
      const data = await authServiceLogin(email, password);
      loginToStore(data.access_token);
      navigate("/");
    } catch (err) {
      setError("Falha na autenticação. Verifique seu e-mail e senha.");
      console.error(err);
    }
  };

  return (
    <main className="flex items-center justify-center min-h-screen bg-gray-50 p-4 sm:p-6 lg:p-8">
      <div className="w-full max-w-md p-8 space-y-6 bg-white sm:rounded-xl sm:shadow-lg">
        <div className="text-center">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900">
            Acesse sua conta
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Bem-vindo ao painel de gerenciamento IBDN.
          </p>
        </div>

        <form className="space-y-6" onSubmit={handleSubmit}>
          {/* ... campos de email e senha ... */}
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700"
            >
              Endereço de e-mail
            </label>
            <div className="mt-1">
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="seuemail@exemplo.com"
              />
            </div>
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-700"
            >
              Senha
            </label>
            <div className="mt-1">
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 placeholder-gray-400 border border-gray-300 rounded-md shadow-sm appearance-none focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="********"
              />
            </div>
          </div>
          {error && (
            <div className="p-3 text-sm text-red-700 bg-red-100 border border-red-400 rounded-md">
              {error}
            </div>
          )}

          <div>
            <button
              type="submit"
              className="flex justify-center w-full px-4 py-2 text-sm font-medium text-white bg-green-900 border border-transparent rounded-md shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Entrar
            </button>
          </div>

          {/* 2. Adicionar o link para a página de registro */}
          <div className="text-sm text-center">
            <p className="text-gray-600">
              Não tem uma conta?{" "}
              <Link
                to="/register"
                className="font-medium text-indigo-600 hover:text-indigo-500"
              >
                Registre-se
              </Link>
            </p>
          </div>
        </form>
      </div>
    </main>
  );
}

export default LoginPage;
