import React, { useState, useEffect } from "react";
import useAuthStore from "../store/authStore"; // Importar a store

function EmpresaForm({ initialData = {}, onSubmit, onCancel, isSaving }) {
  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState({});

  // NOVO: Obter permissões do usuário logado
  const permissions = useAuthStore((state) => state.permissions);
  const isAdmin =
    permissions.includes("admin") || permissions.includes("admin_master");

  useEffect(() => {
    setFormData({
      cnpj: initialData.cnpj || "",
      razao_social: initialData.razao_social || "",
      nome_fantasia: initialData.nome_fantasia || "",
      telefone: initialData.telefone || "",
      responsavel: initialData.responsavel || "",
      cargo_responsavel: initialData.cargo_responsavel || "",
      site_empresa: initialData.site_empresa || "",
      ativo: initialData.ativo !== undefined ? initialData.ativo : true,
      usuario_id: initialData.usuario_id || "",
    });
    setErrors({});
  }, [initialData]);

  const handleChange = (e) => {
    // ...
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const dataToSubmit = { ...formData };
    // Remove o campo usuario_id se estiver vazio ou se o usuário não for admin
    if (!dataToSubmit.usuario_id || !isAdmin) {
      delete dataToSubmit.usuario_id;
    }
    onSubmit(dataToSubmit);
  };

  const isEditing = !!initialData.id;

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2">
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
            onChange={handleChange}
            disabled={isEditing}
            className={`mt-1 block w-full rounded-md shadow-sm sm:text-sm ${
              errors.cnpj ? "border-red-500" : "border-gray-300"
            } ${isEditing ? "bg-gray-100 cursor-not-allowed" : ""}`}
          />
          {isEditing && (
            <p className="mt-1 text-xs text-gray-500">
              Para alterar o CNPJ, entre em contato com o suporte.
            </p>
          )}
        </div>

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
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm"
          />
        </div>

        {/* MODIFICAÇÃO: Exibir campo de ID do usuário apenas para admins e na criação */}
        {isAdmin && !isEditing && (
          <div className="sm:col-span-2">
            <label
              htmlFor="usuario_id"
              className="block text-sm font-medium text-gray-700"
            >
              ID do Usuário (Opcional - para Admins)
            </label>
            <input
              type="text"
              name="usuario_id"
              id="usuario_id"
              value={formData.usuario_id}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              placeholder="Deixe em branco para associar ao seu próprio usuário"
            />
          </div>
        )}

        {/* ... restante dos campos do formulário ... */}
      </div>
      <div className="flex justify-end space-x-4 pt-4">
        <button
          type="button"
          onClick={onCancel}
          disabled={isSaving}
          className="..."
        >
          Cancelar
        </button>
        <button type="submit" disabled={isSaving} className="...">
          {isSaving ? "Salvando..." : "Salvar"}
        </button>
      </div>
    </form>
  );
}

export default EmpresaForm;
