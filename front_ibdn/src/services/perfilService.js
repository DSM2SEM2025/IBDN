import api from './api';

/**
 * Busca uma lista de todos os perfis.
 * @returns {Promise<Array>} Uma lista de perfis.
 */
export const listarPerfis = async () => {
    try {
        const response = await api.get('/perfis/');
        return response.data;
    } catch (error) {
        console.error('Erro ao listar perfis:', error.response?.data || error.message);
        throw error;
    }
};

/**
 * Cria um novo perfil.
 * @param {Object} dadosPerfil - Os dados do novo perfil (ex: { nome, permissoes_ids: [] }).
 * @returns {Promise<Object>} Os dados do perfil criado.
 */
export const criarPerfil = async (dadosPerfil) => {
    try {
        const response = await api.post('/perfis/', dadosPerfil);
        return response.data;
    } catch (error) {
        console.error('Erro ao criar perfil:', error.response?.data || error.message);
        throw error;
    }
};

/**
 * Atualiza os dados de um perfil existente, incluindo suas permissões.
 * @param {string} perfilId - O ID do perfil a ser atualizado.
 * @param {Object} dadosAtualizacao - Os dados a serem atualizados (ex: { nome, permissoes_ids: [...] }).
 * @returns {Promise<Object>} Os dados do perfil atualizado.
 */
export const atualizarPerfil = async (perfilId, dadosAtualizacao) => {
    try {
        // Esta função agora pode atualizar tanto o nome quanto as permissões em uma única chamada.
        const response = await api.put(`/perfis/${perfilId}`, dadosAtualizacao);
        return response.data;
    } catch (error) {
        console.error(`Erro ao atualizar perfil com ID ${perfilId}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Exclui um perfil.
 * @param {string} perfilId - O ID do perfil a ser excluído.
 * @returns {Promise<Object>} A resposta da API.
 */
export const deletarPerfil = async (perfilId) => {
    try {
        const response = await api.delete(`/perfis/${perfilId}`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao deletar perfil com ID ${perfilId}:`, error.response?.data || error.message);
        throw error;
    }
};

// As funções abaixo (adicionar/remover) ainda podem ser úteis para outras funcionalidades,
// mas não são mais necessárias para a lógica do formulário principal de gestão de permissões.

/**
 * Adiciona uma permissão a um perfil específico.
 * @param {string} perfilId - O ID do perfil.
 * @param {string} permissaoId - O ID da permissão a ser adicionada.
 * @returns {Promise<Object>} O perfil atualizado.
 */
export const adicionarPermissaoAoPerfil = async (perfilId, permissaoId) => {
    try {
        const response = await api.post(`/perfis/${perfilId}/permissoes`, { permissao_id: permissaoId });
        return response.data;
    } catch (error) {
        console.error(`Erro ao adicionar permissão ${permissaoId} ao perfil ${perfilId}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Remove uma permissão de um perfil específico.
 * @param {string} perfilId - O ID do perfil.
 * @param {string} permissaoId - O ID da permissão a ser removida.
 * @returns {Promise<Object>} O perfil atualizado.
 */
export const removerPermissaoDoPerfil = async (perfilId, permissaoId) => {
    try {
        const response = await api.delete(`/perfis/${perfilId}/permissoes/${permissaoId}`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao remover permissão ${permissaoId} do perfil ${perfilId}:`, error.response?.data || error.message);
        throw error;
    }
};