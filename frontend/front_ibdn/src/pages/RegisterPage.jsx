import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { register } from "../services/userService";

function RegisterPage() {
  const [formData, setFormData] = useState({
    nome: "",
    email: "",
    senha: "",
    senha_confirmacao: "",
  });
  // O estado de erro agora é um objeto para guardar mensagens para cada campo
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Limpa o erro do campo quando o usuário começa a digitar
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: null }));
    }
  };

  /**
   * Função para validar os dados do formulário antes do envio.
   * @returns {Object} Um objeto contendo os erros de validação.
   */
  const validateForm = () => {
    const newErrors = {};

    // Validação da senha (mínimo de 8 caracteres)
    if (formData.senha.length < 8) {
      newErrors.senha = "A senha deve ter no mínimo 8 caracteres.";
    }

    // Validação da confirmação de senha
    if (formData.senha !== formData.senha_confirmacao) {
      newErrors.senha_confirmacao = "As senhas não coincidem.";
    }

    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccess("");

    // 1. Executa a validação
    const validationErrors = validateForm();
    if (Object.keys(validationErrors).length > 0) {
      // 2. Se houver erros, atualiza o estado de erros e interrompe o envio
      setErrors(validationErrors);
      return;
    }

    // 3. Se tudo estiver certo, limpa os erros e prossegue com o envio
    setErrors({});
    setLoading(true);
    try {
      await register(formData);
      setSuccess(
        "Registro realizado com sucesso! Você será redirecionado para o login."
      );
      setTimeout(() => {
        navigate("/login");
      }, 3000);
    } catch (err) {
      setErrors({
        api: err.detail || "Falha ao realizar o registro. Tente novamente.",
      });
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
            Preencha os campos para se registrar na plataforma.
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
              placeholder="Mínimo 8 caracteres"
            />
            {/* Exibição da mensagem de erro específica para a senha */}
            {errors.senha && (
              <p className="mt-1 text-xs text-red-600">{errors.senha}</p>
            )}
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
            {/* Exibição da mensagem de erro específica para a confirmação */}
            {errors.senha_confirmacao && (
              <p className="mt-1 text-xs text-red-600">
                {errors.senha_confirmacao}
              </p>
            )}
          </div>

          {/* Mensagens de Sucesso ou Erro geral da API */}
          {errors.api && (
            <div className="p-3 text-sm text-red-700 bg-red-100 border border-red-400 rounded-md">
              {errors.api}
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
              className="flex justify-center w-full px-4 py-2 text-sm font-medium text-white bg-green-900 border border-transparent rounded-md shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {loading ? "Registrando..." : "Registrar"}
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
