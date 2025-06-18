import React, { useState, useEffect } from "react";
import useAuthStore from "../store/authStore";

function EmpresaForm({ initialData = {}, onSubmit, onCancel, isSaving }) {
  // Estado inicial bem definido para evitar erros
  const [formData, setFormData] = useState({
    cnpj: "",
    razao_social: "",
    nome_fantasia: "",
    telefone: "",
    responsavel: "",
    cargo_responsavel: "",
    site: "",
    usuario_id: "",
  });

  const { user } = useAuthStore();
  const isAdmin =
    user &&
    (user.permissoes.includes("admin") ||
      user.permissoes.includes("admin_master"));

  const isEditing = !!initialData.id;

  // Preenche o formulário quando os dados iniciais são fornecidos (para edição)
  useEffect(() => {
    if (initialData.id) {
      setFormData({
        cnpj: initialData.cnpj || "",
        razao_social: initialData.razao_social || "",
        nome_fantasia: initialData.nome_fantasia || "",
        telefone: initialData.telefone || "",
        responsavel: initialData.responsavel || "",
        cargo_responsavel: initialData.cargo_responsavel || "",
        site: initialData.site || "",
        usuario_id: initialData.usuario_id || "",
      });
    }
  }, [initialData]);

  // *** ESTA É A FUNÇÃO QUE FALTAVA ***
  // Ela atualiza o estado do formulário a cada alteração nos inputs.
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const dataToSubmit = { ...formData };

    if (!isAdmin || !dataToSubmit.usuario_id) {
      delete dataToSubmit.usuario_id;
    }

    onSubmit(dataToSubmit);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2">
        {/* Campo CNPJ */}
        <div>
          <label
            htmlFor="cnpj"
            className="block text-sm font-medium text-gray-700"
          >
            CNPJ
          </label>
          <input
            type="text"
            name="cnpj"
            id="cnpj"
            value={formData.cnpj}
            onChange={handleChange} // onChange é necessário para campos controlados
            required
            disabled={isEditing}
            className={`mt-1 block w-full rounded-md shadow-sm sm:text-sm border-gray-300 ${
              isEditing ? "bg-gray-100 cursor-not-allowed" : ""
            }`}
          />
          {isEditing && (
            <p className="mt-1 text-xs text-gray-500">
              O CNPJ não pode ser alterado.
            </p>
          )}
        </div>

        {/* Campo Razão Social */}
        <div>
          <label
            htmlFor="razao_social"
            className="block text-sm font-medium text-gray-700"
          >
            Razão Social
          </label>
          <input
            type="text"
            name="razao_social"
            id="razao_social"
            value={formData.razao_social}
            onChange={handleChange} // onChange é necessário
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>

        {/* Restante do formulário */}
        <div className="sm:col-span-2">
          <label
            htmlFor="nome_fantasia"
            className="block text-sm font-medium text-gray-700"
          >
            Nome Fantasia
          </label>
          <input
            type="text"
            name="nome_fantasia"
            id="nome_fantasia"
            value={formData.nome_fantasia}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
        <div>
          <label
            htmlFor="responsavel"
            className="block text-sm font-medium text-gray-700"
          >
            Responsável
          </label>
          <input
            type="text"
            name="responsavel"
            id="responsavel"
            value={formData.responsavel}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
        <div>
          <label
            htmlFor="cargo_responsavel"
            className="block text-sm font-medium text-gray-700"
          >
            Cargo do Responsável
          </label>
          <input
            type="text"
            name="cargo_responsavel"
            id="cargo_responsavel"
            value={formData.cargo_responsavel}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
        <div>
          <label
            htmlFor="telefone"
            className="block text-sm font-medium text-gray-700"
          >
            Telefone
          </label>
          <input
            type="text"
            name="telefone"
            id="telefone"
            value={formData.telefone}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
        <div>
          <label
            htmlFor="site"
            className="block text-sm font-medium text-gray-700"
          >
            Site
          </label>
          <input
            type="url"
            name="site"
            id="site"
            value={formData.site}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            placeholder="https://exemplo.com"
          />
        </div>

        {isAdmin && (
          <div className="flex items-center sm:col-span-2">
            <input
              id="ativo"
              name="ativo"
              type="checkbox"
              checked={formData.ativo}
              onChange={handleChange}
              className="h-4 w-4 rounded border-gray-300 text-indigo-600"
            />
            <label htmlFor="ativo" className="ml-2 block text-sm text-gray-900">
              Empresa Ativa
            </label>
          </div>
        )}
      </div>

      <div className="flex justify-end space-x-4 pt-4">
        <button
          type="button"
          onClick={onCancel}
          disabled={isSaving}
          className="rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={isSaving}
          className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700"
        >
          {isSaving ? "Aguarde..." : "Salvar Empresa"}
        </button>
      </div>
    </form>
  );
}

export default EmpresaForm;
