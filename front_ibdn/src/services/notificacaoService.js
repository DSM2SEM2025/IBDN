import api from './api';

/**
 * Busca a lista de notificações de uma empresa específica.
 * @param {number} idEmpresa - O ID da empresa.
 * @param {boolean} [lida] - Filtra por status de lida (opcional).
 * @returns {Promise<Array>} Uma lista de notificações.
 */
export const listarNotificacoesEmpresa = async (idEmpresa, lida = null) => {
    try {
        const params = {};
        if (lida !== null) {
            params.lida = lida;
        }
        const response = await api.get(`/empresas/${idEmpresa}/notificacoes`, { params });
        return response.data;
    } catch (error) {
        console.error(`Erro ao buscar notificações para a empresa ${idEmpresa}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Cria uma nova notificação para uma empresa.
 * @param {number} idEmpresa - O ID da empresa.
 * @param {Object} dadosNotificacao - Os dados da nova notificação ({ mensagem, tipo }).
 * @returns {Promise<Object>} A resposta da API.
 */
export const criarNotificacao = async (idEmpresa, dadosNotificacao) => {
    try {
        const response = await api.post(`/empresas/${idEmpresa}/notificacoes`, dadosNotificacao);
        return response.data;
    } catch (error) {
        console.error(`Erro ao criar notificação para a empresa ${idEmpresa}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Atualiza uma notificação (ex: marcar como lida).
 * @param {number} idNotificacao - O ID da notificação.
 * @param {Object} dadosAtualizacao - Os dados a serem atualizados (ex: { lida: true }).
 * @returns {Promise<Object>} A resposta da API.
 */
export const atualizarNotificacao = async (idNotificacao, dadosAtualizacao) => {
    try {
        const response = await api.put(`/notificacoes/${idNotificacao}`, dadosAtualizacao);
        return response.data;
    } catch (error) {
        console.error(`Erro ao atualizar notificação ${idNotificacao}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Deleta uma notificação.
 * @param {number} idNotificacao - O ID da notificação.
 * @returns {Promise<Object>} A resposta da API.
 */
export const deletarNotificacao = async (idNotificacao) => {
    try {
        const response = await api.delete(`/notificacoes/${idNotificacao}`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao deletar notificação ${idNotificacao}:`, error.response?.data || error.message);
        throw error;
    }
};
