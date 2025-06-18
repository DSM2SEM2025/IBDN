import api from './api';

/**
 * Busca uma lista de todos os utilizadores.
 * @returns {Promise<Array>} Uma lista de utilizadores.
 */
export const listarUsuarios = async () => {
    try {
        const response = await api.get('/usuario/');
        return response.data;
    } catch (error) {
        console.error('Erro ao listar utilizadores:', error.response?.data || error.message);
        throw error;
    }
};

/**
 * Cria um novo utilizador.
 * @param {Object} dadosUsuario - Os dados do novo utilizador (conforme schema IbdnUsuarioCreate).
 * @returns {Promise<Object>} Os dados do utilizador criado.
 */
export const criarUsuario = async (dadosUsuario) => {
    try {
        const response = await api.post('/usuario/', dadosUsuario);
        return response.data;
    } catch (error) {
        console.error('Erro ao criar utilizador:', error.response?.data || error.message);
        throw error;
    }
};

/**
 * Atualiza os dados de um utilizador existente.
 * @param {string} usuarioId - O ID do utilizador a ser atualizado.
 * @param {Object} dadosAtualizacao - Os dados a serem atualizados (conforme schema IbdnUsuarioUpdate).
 * @returns {Promise<Object>} Os dados do utilizador atualizado.
 */
export const atualizarUsuario = async (usuarioId, dadosAtualizacao) => {
    try {
        const response = await api.put(`/usuario/${usuarioId}`, dadosAtualizacao);
        return response.data;
    } catch (error) {
        console.error(`Erro ao atualizar utilizador com ID ${usuarioId}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Exclui um utilizador.
 * @param {string} usuarioId - O ID do utilizador a ser excluído.
 * @returns {Promise<Object>} A resposta da API.
 */
export const deletarUsuario = async (usuarioId) => {
    try {
        const response = await api.delete(`/usuario/${usuarioId}`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao deletar utilizador com ID ${usuarioId}:`, error.response?.data || error.message);
        throw error;
    }
};
