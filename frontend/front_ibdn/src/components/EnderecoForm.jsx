import React, { useState, useEffect } from "react";

/**
 * Formulário para editar um endereço de uma empresa.
 * @param {Object} props
 * @param {Object} props.initialData - Os dados do endereço a ser editado.
 * @param {Function} props.onSubmit - Função chamada ao submeter o formulário.
 * @param {Function} props.onCancel - Função para cancelar e fechar.
 * @param {boolean} props.isSaving - Indica se o processo de salvar está em andamento.
 */
function EnderecoForm({ initialData, onSubmit, onCancel, isSaving }) {
  const [formData, setFormData] = useState({
    logradouro: "",
    bairro: "",
    cep: "",
    cidade: "",
    uf: "",
    complemento: "",
  });

  // Efeito para preencher o formulário com os dados iniciais
  useEffect(() => {
    if (initialData) {
      setFormData({
        logradouro: initialData.logradouro || "",
        bairro: initialData.bairro || "",
        cep: initialData.cep || "",
        cidade: initialData.cidade || "",
        uf: initialData.uf || "",
        complemento: initialData.complemento || "",
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
        {/* Campo Logradouro */}
        <div className="sm:col-span-2">
          <label
            htmlFor="logradouro"
            className="block text-sm font-medium text-gray-700"
          >
            Logradouro
          </label>
          <input
            type="text"
            name="logradouro"
            id="logradouro"
            value={formData.logradouro}
            onChange={handleChange}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        {/* Campo Bairro */}
        <div>
          <label
            htmlFor="bairro"
            className="block text-sm font-medium text-gray-700"
          >
            Bairro
          </label>
          <input
            type="text"
            name="bairro"
            id="bairro"
            value={formData.bairro}
            onChange={handleChange}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        {/* Campo CEP */}
        <div>
          <label
            htmlFor="cep"
            className="block text-sm font-medium text-gray-700"
          >
            CEP
          </label>
          <input
            type="text"
            name="cep"
            id="cep"
            value={formData.cep}
            onChange={handleChange}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        {/* Campo Cidade */}
        <div>
          <label
            htmlFor="cidade"
            className="block text-sm font-medium text-gray-700"
          >
            Cidade
          </label>
          <input
            type="text"
            name="cidade"
            id="cidade"
            value={formData.cidade}
            onChange={handleChange}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        {/* Campo UF */}
        <div>
          <label
            htmlFor="uf"
            className="block text-sm font-medium text-gray-700"
          >
            UF
          </label>
          <input
            type="text"
            name="uf"
            id="uf"
            value={formData.uf}
            onChange={handleChange}
            required
            maxLength="2"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        {/* Campo Complemento */}
        <div className="sm:col-span-2">
          <label
            htmlFor="complemento"
            className="block text-sm font-medium text-gray-700"
          >
            Complemento
          </label>
          <input
            type="text"
            name="complemento"
            id="complemento"
            value={formData.complemento}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
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
          {isSaving ? "Salvando..." : "Salvar Endereço"}
        </button>
      </div>
    </form>
  );
}

export default EnderecoForm;
