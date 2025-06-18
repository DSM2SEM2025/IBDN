// front_e_back/src/components/EnderecoForm.jsx
import React, { useState, useRef } from "react";

/**
 * Formulário de Endereço "controlado", que recebe os seus dados e funções via props.
 * @param {Object} props
 * @param {Object} props.formData - O objeto com os dados do formulário (controlado pelo pai).
 * @param {Function} props.setFormData - A função para atualizar o estado no componente pai.
 * @param {Function} props.onSubmit - Função chamada ao submeter o formulário.
 * @param {Function} props.onCancel - Função para cancelar.
 * @param {boolean} props.isSaving - Indica se está a salvar.
 */
function EnderecoForm({ formData, setFormData, onSubmit, onCancel, isSaving }) {
  // Estado local apenas para a lógica do CEP
  const [cepLoading, setCepLoading] = useState(false);
  const [cepError, setCepError] = useState("");
  const numeroInputRef = useRef(null);

  const isEditing = !!formData.id; // Verifica se está em modo de edição

  // A função handleChange agora chama a função setFormData do componente pai
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleCepBlur = async (e) => {
    const cep = e.target.value.replace(/\D/g, "");
    if (cep.length !== 8) {
      if (cep.length > 0) setCepError("CEP inválido.");
      else setCepError("");
      return;
    }
    setCepError("");
    setCepLoading(true);
    try {
      const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
      const data = await response.json();
      if (data.erro) {
        setCepError("CEP não encontrado.");
      } else {
        // Atualiza o estado no componente pai com os dados do ViaCEP
        setFormData((prev) => ({
          ...prev,
          logradouro: data.logradouro,
          bairro: data.bairro,
          cidade: data.localidade,
          uf: data.uf,
        }));
        numeroInputRef.current?.focus();
      }
    } catch (error) {
      setCepError("Erro ao buscar CEP.");
    } finally {
      setCepLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-6">
        <div className="sm:col-span-2">
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
            onBlur={handleCepBlur}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
          {cepLoading && <p className="text-sm text-gray-500">A procurar...</p>}
          {cepError && <p className="text-sm text-red-600">{cepError}</p>}
        </div>

        <div className="sm:col-span-4">
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
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>

        <div className="sm:col-span-2">
          <label
            htmlFor="numero"
            className="block text-sm font-medium text-gray-700"
          >
            Número
          </label>
          <input
            type="text"
            name="numero"
            id="numero"
            ref={numeroInputRef}
            value={formData.numero}
            onChange={handleChange}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>

        <div className="sm:col-span-4">
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
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>

        <div className="sm:col-span-6">
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
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>

        <div className="sm:col-span-4">
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
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>

        <div className="sm:col-span-2">
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
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
      </div>

      <div className="flex justify-end space-x-4 pt-4">
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            disabled={isSaving}
            className="rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50"
          >
            Voltar
          </button>
        )}
        <button
          type="submit"
          disabled={isSaving || cepLoading}
          className="inline-flex justify-center rounded-md border border-transparent bg-green-900 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-green-700 disabled:opacity-50"
        >
          {isSaving
            ? "Aguarde..."
            : isEditing
            ? "Salvar Endereço"
            : "Avançar para Ramos"}
        </button>
      </div>
    </form>
  );
}

export default EnderecoForm;
