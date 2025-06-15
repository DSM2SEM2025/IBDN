import React, { useState, useEffect } from "react";

/**
 * Formulário para criar ou editar uma empresa.
 * @param {Object} props
 * @param {Object} [props.initialData={}] - Os dados iniciais para preencher o formulário (para edição).
 * @param {Function} props.onSubmit - Função chamada ao submeter o formulário.
 * @param {Function} props.onCancel - Função chamada para cancelar e fechar o formulário.
 * @param {boolean} props.isSaving - Indica se o processo de salvar está em andamento.
 */
function EmpresaForm({ initialData = {}, onSubmit, onCancel, isSaving }) {
  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState({});

  // Efeito para inicializar o formulário quando os dados iniciais mudam
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
      // Não incluímos usuario_id aqui, pois será gerenciado pelo backend
    });
    // Limpa os erros ao mudar os dados
    setErrors({});
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
    // Limpa o erro do campo ao ser modificado
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: null }));
    }
  };

  const validate = () => {
    const newErrors = {};
    const cnpjRegex = /^(\d{2}\.?\d{3}\.?\d{3}\/\d{4}-?\d{2})$/;

    if (!formData.cnpj) {
      newErrors.cnpj = "O CNPJ é obrigatório.";
    } else if (!cnpjRegex.test(formData.cnpj)) {
      newErrors.cnpj = "Formato de CNPJ inválido. Use XX.XXX.XXX/XXXX-XX.";
    }

    if (!formData.razao_social) {
      newErrors.razao_social = "A Razão Social é obrigatória.";
    }

    if (formData.site_empresa) {
      try {
        new URL(formData.site_empresa);
      } catch (_) {
        newErrors.site_empresa = "URL do site inválida.";
      }
    }

    setErrors(newErrors);
    // Retorna true se não houver erros
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
    }
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
            onChange={handleChange}
            className={`mt-1 block w-full rounded-md shadow-sm sm:text-sm ${
              errors.cnpj ? "border-red-500" : "border-gray-300"
            }`}
          />
          {errors.cnpj && (
            <p className="mt-2 text-sm text-red-600">{errors.cnpj}</p>
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
            onChange={handleChange}
            className={`mt-1 block w-full rounded-md shadow-sm sm:text-sm ${
              errors.razao_social ? "border-red-500" : "border-gray-300"
            }`}
          />
          {errors.razao_social && (
            <p className="mt-2 text-sm text-red-600">{errors.razao_social}</p>
          )}
        </div>

        {/* O resto dos campos segue o mesmo padrão... */}
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
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
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
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
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
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
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
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        <div>
          <label
            htmlFor="site_empresa"
            className="block text-sm font-medium text-gray-700"
          >
            Site
          </label>
          <input
            type="url"
            name="site_empresa"
            id="site_empresa"
            value={formData.site_empresa}
            onChange={handleChange}
            className={`mt-1 block w-full rounded-md shadow-sm sm:text-sm ${
              errors.site_empresa ? "border-red-500" : "border-gray-300"
            }`}
            placeholder="https://exemplo.com"
          />
          {errors.site_empresa && (
            <p className="mt-2 text-sm text-red-600">{errors.site_empresa}</p>
          )}
        </div>

        {/* Campo Ativo */}
        <div className="flex items-center sm:col-span-2">
          <input
            id="ativo"
            name="ativo"
            type="checkbox"
            checked={formData.ativo}
            onChange={handleChange}
            className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
          />
          <label htmlFor="ativo" className="ml-2 block text-sm text-gray-900">
            Empresa Ativa
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
          className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {isSaving ? "Salvando..." : "Salvar Alterações"}
        </button>
      </div>
    </form>
  );
}

export default EmpresaForm;
