import api from './api';

/**
 * Busca a lista de endereços associados a uma empresa específica.
 * @param {number} idEmpresa - O ID da empresa.
 * @returns {Promise<Array>} Uma lista de endereços.
 */
export const listarEnderecosDaEmpresa = async (idEmpresa) => {
    try {
        const response = await api.get(`/empresas/${idEmpresa}/enderecos`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao buscar endereços para a empresa ${idEmpresa}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Atualiza um endereço específico de uma empresa.
 * @param {number} idEmpresa - O ID da empresa.
 * @param {number} idEndereco - O ID do endereço a ser atualizado.
 * @param {Object} dadosAtualizacao - Os dados do endereço a serem atualizados.
 * @returns {Promise<Object>} A resposta da API.
 */
export const atualizarEnderecoDaEmpresa = async (idEmpresa, idEndereco, dadosAtualizacao) => {
    try {
        const response = await api.put(`/empresas/${idEmpresa}/enderecos/${idEndereco}`, dadosAtualizacao);
        return response.data;
    } catch (error) {
        console.error(`Erro ao atualizar endereço ${idEndereco} da empresa ${idEmpresa}:`, error.response?.data || error.message);
        throw error;
    }
};
