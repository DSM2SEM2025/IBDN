// front_e_back/src/services/seloService.js
import api from './api';

/**
 * Busca uma lista de todos os selos e as empresas associadas.
 * Esta função é geralmente usada por administradores para ter uma visão geral.
 * @returns {Promise<Array>} Uma lista de selos com detalhes da empresa e do tipo de selo.
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

/**
 * Busca os selos concedidos a uma empresa específica.
 * Usado tanto por administradores (para qualquer empresa) quanto por empresas (para si mesmas).
 * @param {number} empresaId - O ID da empresa.
 * @returns {Promise<Array>} Uma lista de selos concedidos à empresa.
 */
export const getSelosByEmpresa = async (empresaId) => {
    try {
        // A rota no backend para listar selos de uma empresa é /empresas/{id_empresa}/selos
        const response = await api.get(`/empresas/${empresaId}/selos`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao buscar selos para a empresa ${empresaId}:`, error.response?.data || error.message);
        throw error;
    }
}

/**
 * Busca todas as solicitações de selo pendentes ou em renovação.
 * Esta função é de uso exclusivo para administradores.
 * @returns {Promise<Array>} Uma lista de solicitações de selo.
 */
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
 * Aprova uma solicitação de selo, alterando seu status para 'Ativo'.
 * Apenas administradores podem realizar esta ação.
 * @param {number} seloId - O ID da instância do selo (da tabela empresa_selo) a ser aprovado.
 * @returns {Promise<Object>} A resposta da API.
 */
export const aprovarSelo = async (seloId) => {
    try {
        // A rota no backend é /empresa-selos/{empresa_selo_id}/aprovar
        const response = await api.put(`/empresa-selos/${seloId}/aprovar`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao aprovar selo com ID ${seloId}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Solicita a renovação de um selo existente.
 * Esta ação é tipicamente realizada por uma empresa para seus próprios selos expirados ou próximos do vencimento.
 * @param {number} seloId - O ID da instância do selo (da tabela empresa_selo).
 * @returns {Promise<Object>} A resposta da API.
 */
export const solicitarRenovacaoSelo = async (seloId) => {
    try {
        // A rota no backend é /empresa-selos/{empresa_selo_id}/solicitar-renovacao
        const response = await api.put(`/empresa-selos/${seloId}/solicitar-renovacao`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao solicitar renovação para o selo ${seloId}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Associa um novo tipo de selo a uma empresa.
 * Esta função é de uso exclusivo para administradores (conceder um selo a uma empresa).
 * @param {number} idEmpresa - O ID da empresa à qual o selo será associado.
 * @param {Object} dadosAssociacao - Os dados para a associação (id_selo: ID do tipo de selo, dias_validade: número de dias de validade).
 * @returns {Promise<Object>} Os dados da associação criada.
 */
export const associarSeloAEmpresa = async (idEmpresa, dadosAssociacao) => {
    try {
        // A rota no backend é /empresas/{id_empresa}/selos para concessão por admin
        const response = await api.post(`/empresas/${idEmpresa}/selos`, dadosAssociacao);
        return response.data;
    } catch (error) {
        console.error(`Erro ao associar selo à empresa ${idEmpresa}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Permite que um usuário com perfil 'empresa' solicite um selo para sua própria empresa.
 * A solicitação é criada com status 'Pendente' e aguarda aprovação de um administrador.
 * @param {number} idSelo - O ID do tipo de selo (do catálogo) que a empresa deseja solicitar.
 * @returns {Promise<Object>} A resposta da API indicando o sucesso da solicitação.
 */
export const solicitarSelo = async (idSelo) => {
    try {
        // Rota específica para a empresa solicitar um selo do catálogo
        const response = await api.post('/selos/solicitar', { id_selo: idSelo });
        return response.data;
    } catch (error) {
        console.error(`Erro ao solicitar selo ${idSelo}:`, error.response?.data || error.message);
        throw error;
    }
};