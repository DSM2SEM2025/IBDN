import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { register } from "../services/userService"; // Importamos a nova função

function RegisterPage() {
  const [formData, setFormData] = useState({
    nome: "",
    email: "",
    senha: "",
    senha_confirmacao: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (formData.senha !== formData.senha_confirmacao) {
      setError("As senhas não coincidem.");
      return;
    }

    setLoading(true);
    try {
      await register(formData);
      setSuccess("registro realizado com sucesso! Pode agora fazer login.");
      setTimeout(() => {
        navigate("/login");
      }, 3000); // Redireciona para o login após 3 segundos
    } catch (err) {
      setError(err.detail || "Falha ao realizar o registro. Tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex items-center justify-center min-h-screen bg-gray-50 p-4">
      <div className="w-full max-w-md p-8 space-y-6 bg-white sm:rounded-xl sm:shadow-lg">
        <div className="text-center">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900">
            Crie a sua conta
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Preencha os campos para se Registrar na plataforma.
          </p>
        </div>

        <form className="space-y-6" onSubmit={handleSubmit}>
          {/* Campo Nome */}
          <div>
            <label
              htmlFor="nome"
              className="block text-sm font-medium text-gray-700"
            >
              Nome Completo
            </label>
            <input
              id="nome"
              name="nome"
              type="text"
              required
              value={formData.nome}
              onChange={handleChange}
              className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm"
              placeholder="Seu Nome Completo"
            />
          </div>

          {/* Campo Email */}
          <div>
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700"
            >
              Endereço de e-mail
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={formData.email}
              onChange={handleChange}
              className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm"
              placeholder="seuemail@exemplo.com"
            />
          </div>

          {/* Campo Senha */}
          <div>
            <label
              htmlFor="senha"
              className="block text-sm font-medium text-gray-700"
            >
              Senha
            </label>
            <input
              id="senha"
              name="senha"
              type="password"
              required
              value={formData.senha}
              onChange={handleChange}
              className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm"
              placeholder="********"
            />
          </div>

          {/* Campo Confirmação de Senha */}
          <div>
            <label
              htmlFor="senha_confirmacao"
              className="block text-sm font-medium text-gray-700"
            >
              Confirme a Senha
            </label>
            <input
              id="senha_confirmacao"
              name="senha_confirmacao"
              type="password"
              required
              value={formData.senha_confirmacao}
              onChange={handleChange}
              className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm"
              placeholder="********"
            />
          </div>

          {/* Mensagens de Erro e Sucesso */}
          {error && (
            <div className="p-3 text-sm text-red-700 bg-red-100 border border-red-400 rounded-md">
              {error}
            </div>
          )}
          {success && (
            <div className="p-3 text-sm text-green-700 bg-green-100 border border-green-400 rounded-md">
              {success}
            </div>
          )}

          {/* Botão de Submissão */}
          <div>
            <button
              type="submit"
              disabled={loading}
              className="flex justify-center w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {loading ? "A Registrar..." : "Registrar"}
            </button>
          </div>

          <div className="text-sm text-center">
            <Link
              to="/login"
              className="font-medium text-indigo-600 hover:text-indigo-500"
            >
              Já tem uma conta? Faça login
            </Link>
          </div>
        </form>
      </div>
    </main>
  );
}

export default RegisterPage;
