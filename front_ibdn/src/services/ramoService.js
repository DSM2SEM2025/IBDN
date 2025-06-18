import api from './api';

/**
 * Busca uma lista de todos os ramos de atividade.
 * @returns {Promise<Array>} Uma lista de ramos.
 */
export const listarRamos = async () => {
    try {
        const response = await api.get('/ramos');
        return response.data;
    } catch (error) {
        console.error('Erro ao listar ramos:', error.response?.data || error.message);
        throw error;
    }
};

/**
 * Cria um novo ramo de atividade.
 * @param {Object} dadosRamo - Os dados do novo ramo (ex: { nome, descricao }).
 * @returns {Promise<Object>} Os dados do ramo criado.
 */
export const criarRamo = async (dadosRamo) => {
    try {
        const response = await api.post('/ramos', dadosRamo);
        return response.data;
    } catch (error) {
        console.error('Erro ao criar ramo:', error.response?.data || error.message);
        throw error;
    }
};

/**
 * Atualiza os dados de um ramo existente.
 * @param {number} ramoId - O ID do ramo a ser atualizado.
 * @param {Object} dadosAtualizacao - Os dados a serem atualizados.
 * @returns {Promise<Object>} Os dados do ramo atualizado.
 */
export const atualizarRamo = async (ramoId, dadosAtualizacao) => {
    try {
        const response = await api.put(`/ramos/${ramoId}`, dadosAtualizacao);
        return response.data;
    } catch (error) {
        console.error(`Erro ao atualizar ramo com ID ${ramoId}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Exclui um ramo de atividade.
 * @param {number} ramoId - O ID do ramo a ser excluído.
 * @returns {Promise<void>}
 */
export const deletarRamo = async (ramoId) => {
    try {
        const response = await api.delete(`/ramos/${ramoId}`);
        return response.data; // O endpoint retorna 204, mas podemos retornar os dados por consistência.
    } catch (error) {
        console.error(`Erro ao deletar ramo com ID ${ramoId}:`, error.response?.data || error.message);
        throw error;
    }
};
