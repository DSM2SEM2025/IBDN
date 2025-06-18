// front_e_back/src/services/empresaService.js
import api from './api';

/**
 * Busca uma lista de todas as empresas.
 * @returns {Promise<Array>} Uma lista de empresas.
 */
export const listarEmpresas = async () => {
    try {
        const response = await api.get('/empresas');
        return response.data;
    } catch (error) {
        console.error('Erro ao listar empresas:', error.response?.data || error.message);
        throw error;
    }
};

/**
 * Busca os detalhes de uma empresa específica pelo seu ID.
 * @param {number} empresaId - O ID da empresa.
 * @returns {Promise<Object>} Os dados da empresa.
 */
export const buscarEmpresaPorId = async (empresaId) => {
    try {
        const response = await api.get(`/empresas/${empresaId}`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao buscar empresa com ID ${empresaId}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Cria uma nova empresa.
 * @param {Object} dadosEmpresa - Os dados da nova empresa (conforme schema EmpresaCreate).
 * @returns {Promise<Object>} Os dados da empresa criada.
 */
export const adicionarEmpresa = async (dadosEmpresa) => {
    try {
        const response = await api.post('/empresas', dadosEmpresa);
        return response.data;
    } catch (error) {
        console.error('Erro ao adicionar empresa:', error.response?.data || error.message);
        throw error;
    }
};

/**
 * Atualiza os dados de uma empresa existente.
 * @param {number} empresaId - O ID da empresa a ser atualizada.
 * @param {Object} dadosAtualizacao - Os dados a serem atualizados (conforme schema EmpresaUpdate).
 * @returns {Promise<Object>} Os dados da empresa atualizada.
 */
export const atualizarEmpresa = async (empresaId, dadosAtualizacao) => {
    try {
        const response = await api.put(`/empresas/${empresaId}`, dadosAtualizacao);
        return response.data;
    } catch (error) {
        console.error(`Erro ao atualizar empresa com ID ${empresaId}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Exclui (logicamente) uma empresa.
 * @param {number} empresaId - O ID da empresa a ser excluída.
 * @returns {Promise<Object>} A resposta da API.
 */
export const excluirEmpresa = async (empresaId) => {
    try {
        const response = await api.delete(`/empresas/${empresaId}`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao excluir empresa com ID ${empresaId}:`, error.response?.data || error.message);
        throw error;
    }
};