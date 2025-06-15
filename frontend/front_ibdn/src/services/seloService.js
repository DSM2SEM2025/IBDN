import api from './api';

/**
 * Busca uma lista de todos os selos e as empresas associadas.
 * @returns {Promise<Array>} Uma lista de selos.
 */
export const listarTodosSelos = async () => {
    try {
        const response = await api.get('/selos/todos_selos');
        return response.data;
    } catch (error) {
        console.error('Erro ao listar todos os selos:', error.response?.data || error.message);
        throw error;
    }
};

// NEW: Function to get seals for a specific company
export const getSelosByEmpresa = async (empresaId) => {
    try {
        const response = await api.get(`/selos/por-empresa/${empresaId}`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao buscar selos para a empresa ${empresaId}:`, error.response?.data || error.message);
        throw error;
    }
}

// NEW: Function to get all pending seal solicitations
export const getSolicitacoesSelo = async () => {
    try {
        const response = await api.get('/selos/solicitacoes');
        return response.data;
    } catch (error) {
        console.error('Erro ao listar solicitações de selo:', error.response?.data || error.message);
        throw error;
    }
}

/**
 * Aprova um selo específico.
 * @param {number} seloId - O ID do selo a ser aprovado.
 * @returns {Promise<Object>} A resposta da API.
 */
export const aprovarSelo = async (seloId) => {
    try {
        // MODIFIED: Endpoint permission changed to admin/admin_master
        const response = await api.put(`/selos/aprovar/${seloId}`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao aprovar selo com ID ${seloId}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Solicita a renovação de um selo.
 * @param {number} seloId - O ID do selo.
 * @returns {Promise<Object>} A resposta da API.
 */
export const solicitarRenovacaoSelo = async (seloId) => {
    try {
        // Corrected the endpoint to match the backend route
        const response = await api.put(`/selos/solicitar_renovacao/${seloId}/`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao solicitar renovação para o selo ${seloId}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Associa um novo selo a uma empresa.
 * @param {number} idEmpresa - O ID da empresa.
 * @param {Object} dadosAssociacao - Os dados para a associação (id_tipo_selo, dias_validade).
 * @returns {Promise<Object>} Os dados da associação criada.
 */
export const associarSeloAEmpresa = async (idEmpresa, dadosAssociacao) => {
    try {
        // MODIFIED: Endpoint permission changed to admin/admin_master
        const response = await api.post(`/selos/${idEmpresa}/associar`, dadosAssociacao);
        return response.data;
    } catch (error) {
        console.error(`Erro ao associar selo à empresa ${idEmpresa}:`, error.response?.data || error.message);
        throw error;
    }
};