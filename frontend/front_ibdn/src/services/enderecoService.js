// front_e_back/src/services/enderecoService.js
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
 * Busca um único endereço de uma empresa.
 * @param {number} idEmpresa - O ID da empresa.
 * @returns {Promise<Object|null>} O objeto do endereço ou null se não for encontrado.
 */
export const getEndereco = async (idEmpresa) => {
    try {
        const response = await api.get(`/empresas/${idEmpresa}/enderecos`);
        // A API retorna uma lista, então pegamos o primeiro item se houver
        return response.data.length > 0 ? response.data[0] : null;
    } catch (error) {
        // Se for um 404, não é um erro de facto, mas sim "não encontrado"
        if (error.response && error.response.status === 404) {
            return null;
        }
        console.error(`Erro ao buscar endereço para a empresa ${idEmpresa}:`, error.response?.data || error.message);
        throw error;
    }
};


/**
 * Cria um novo endereço para uma empresa.
 * @param {number} idEmpresa - O ID da empresa à qual o endereço será associado.
 * @param {Object} dadosEndereco - Os dados do novo endereço.
 * @returns {Promise<Object>} A resposta da API.
 */
export const criarEndereco = async (idEmpresa, dadosEndereco) => {
    try {
        const response = await api.post(`/empresas/${idEmpresa}/endereco`, dadosEndereco);
        return response.data;
    } catch (error) {
        console.error(`Erro ao criar endereço para a empresa ${idEmpresa}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Atualiza um endereço específico de uma empresa.
 * @param {number} idEmpresa - O ID da empresa.
 * @param {Object} dadosAtualizacao - Os dados do endereço a serem atualizados.
 * @returns {Promise<Object>} A resposta da API.
 */
export const atualizarEndereco = async (idEmpresa, dadosAtualizacao) => {
    try {
        // CORREÇÃO: A rota PUT agora espera apenas o id_empresa, pois só há um endereço por empresa
        const response = await api.put(`/empresas/${idEmpresa}/endereco`, dadosAtualizacao);
        return response.data;
    } catch (error) {
        console.error(`Erro ao atualizar endereço da empresa ${idEmpresa}:`, error.response?.data || error.message);
        throw error;
    }
};


/**
 * Deleta um endereço específico de uma empresa.
 * @param {number} idEmpresa - O ID da empresa.
 * @returns {Promise<Object>} A resposta da API.
 */
export const deletarEndereco = async (idEmpresa) => {
    try {
        const response = await api.delete(`/empresas/${idEmpresa}/endereco`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao deletar endereço da empresa ${idEmpresa}:`, error.response?.data || error.message);
        throw error;
    }
};