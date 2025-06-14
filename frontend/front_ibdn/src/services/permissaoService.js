import api from './api';

/**
 * Busca uma lista de todas as permissões.
 * @returns {Promise<Array>} Uma lista de permissões.
 */
export const listarPermissoes = async () => {
    try {
        const response = await api.get('/permissoes/');
        return response.data;
    } catch (error) {
        console.error('Erro ao listar permissões:', error.response?.data || error.message);
        throw error;
    }
};

/**
 * Cria uma nova permissão.
 * @param {Object} dadosPermissao - Os dados da nova permissão (ex: { nome }).
 * @returns {Promise<Object>} Os dados da permissão criada.
 */
export const criarPermissao = async (dadosPermissao) => {
    try {
        const response = await api.post('/permissoes/', dadosPermissao);
        return response.data;
    } catch (error) {
        console.error('Erro ao criar permissão:', error.response?.data || error.message);
        throw error;
    }
};

/**
 * Atualiza os dados de uma permissão existente.
 * @param {string} permissaoId - O ID da permissão a ser atualizada.
 * @param {Object} dadosAtualizacao - Os dados a serem atualizados.
 * @returns {Promise<Object>} Os dados da permissão atualizada.
 */
export const atualizarPermissao = async (permissaoId, dadosAtualizacao) => {
    try {
        const response = await api.put(`/permissoes/${permissaoId}`, dadosAtualizacao);
        return response.data;
    } catch (error) {
        console.error(`Erro ao atualizar permissão com ID ${permissaoId}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Exclui uma permissão.
 * @param {string} permissaoId - O ID da permissão a ser excluída.
 * @returns {Promise<Object>} A resposta da API.
 */
export const deletarPermissao = async (permissaoId) => {
    try {
        const response = await api.delete(`/permissoes/${permissaoId}`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao deletar permissão com ID ${permissaoId}:`, error.response?.data || error.message);
        throw error;
    }
};