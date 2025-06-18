import React, { useState, useEffect } from "react";

/**
 * Formulário para criar ou editar um utilizador.
 * @param {Object} props
 * @param {Object} [props.initialData={}] - Os dados iniciais para preencher (para edição).
 * @param {Array} props.perfis - A lista de todos os perfis disponíveis para seleção.
 * @param {Function} props.onSubmit - Função chamada ao submeter o formulário.
 * @param {Function} props.onCancel - Função para cancelar e fechar.
 * @param {boolean} props.isSaving - Indica se o processo de salvar está em andamento.
 */
function UsuarioForm({
  initialData = {},
  perfis = [],
  onSubmit,
  onCancel,
  isSaving,
}) {
  const [formData, setFormData] = useState({
    nome: "",
    email: "",
    senha: "",
    perfil_id: "",
    ativo: true,
  });

  // Determina se estamos no modo de edição (se initialData tem um ID)
  const isEditing = !!initialData.id;

  // Efeito para preencher o formulário com os dados iniciais no modo de edição
  useEffect(() => {
    if (isEditing) {
      setFormData({
        nome: initialData.nome || "",
        email: initialData.email || "",
        senha: "", // Senha não é preenchida na edição por segurança
        perfil_id: initialData.perfil?.id || "",
        ativo: initialData.ativo !== undefined ? initialData.ativo : true,
      });
    }
  }, [initialData, isEditing]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Cria uma cópia dos dados para não enviar campos vazios desnecessários
    const dataToSubmit = { ...formData };
    if (isEditing && !dataToSubmit.senha) {
      // Se estiver a editar e a senha estiver vazia, não a envie
      delete dataToSubmit.senha;
    }
    onSubmit(dataToSubmit);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
        {/* Campo Nome */}
        <div className="sm:col-span-2">
          <label
            htmlFor="nome"
            className="block text-sm font-medium text-gray-700"
          >
            Nome Completo
          </label>
          <input
            type="text"
            name="nome"
            id="nome"
            value={formData.nome}
            onChange={handleChange}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        {/* Campo E-mail */}
        <div>
          <label
            htmlFor="email"
            className="block text-sm font-medium text-gray-700"
          >
            E-mail
          </label>
          <input
            type="email"
            name="email"
            id="email"
            value={formData.email}
            onChange={handleChange}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
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
            type="password"
            name="senha"
            id="senha"
            value={formData.senha}
            onChange={handleChange}
            required={!isEditing} // Senha é obrigatória apenas na criação
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            placeholder={
              isEditing ? "Deixe em branco para não alterar" : "********"
            }
          />
        </div>

        {/* Campo Seleção de Perfil */}
        <div>
          <label
            htmlFor="perfil_id"
            className="block text-sm font-medium text-gray-700"
          >
            Perfil
          </label>
          <select
            id="perfil_id"
            name="perfil_id"
            value={formData.perfil_id}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
          >
            <option value="">Sem Perfil</option>
            {perfis.map((perfil) => (
              <option key={perfil.id} value={perfil.id}>
                {perfil.nome}
              </option>
            ))}
          </select>
        </div>

        {/* Campo Ativo */}
        <div className="flex items-center pt-2">
          <input
            id="ativo"
            name="ativo"
            type="checkbox"
            checked={formData.ativo}
            onChange={handleChange}
            className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
          />
          <label htmlFor="ativo" className="ml-2 block text-sm text-gray-900">
            Utilizador Ativo
          </label>
        </div>
      </div>

      {/* Botões de Ação */}
      <div className="flex justify-end space-x-4 pt-4">
        <button
          type="button"
          onClick={onCancel}
          disabled={isSaving}
          className="rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={isSaving}
          className="inline-flex justify-center rounded-md border border-transparent bg-green-900 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {isSaving ? "Salvando..." : "Salvar"}
        </button>
      </div>
    </form>
  );
}

export default UsuarioForm;
