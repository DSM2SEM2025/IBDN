import api from './api';

/**
 * Busca uma lista de todos os selos e as empresas associadas.
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
 * ESTA É A FUNÇÃO QUE ESTÁ CAUSANDO O ERRO.
 */
export const getSelosByEmpresa = async (empresaId) => {
    try {
        const response = await api.get(`/empresas/${empresaId}/selos`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao buscar selos para a empresa ${empresaId}:`, error.response?.data || error.message);
        throw error;
    }
}

/**
 * Busca todas as solicitações de selo pendentes ou em renovação.
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
 * Aprova uma solicitação de selo.
 */
export const aprovarSelo = async (seloId) => {
    try {
        const response = await api.put(`/empresa-selos/${seloId}/aprovar`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao aprovar selo com ID ${seloId}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Recusa uma solicitação de selo.
 */
export const recusarSelo = async (seloId) => {
    try {
        const response = await api.put(`/empresa-selos/${seloId}/recusar`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao recusar selo com ID ${seloId}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Solicita a renovação de um selo existente.
 */
export const solicitarRenovacaoSelo = async (seloId) => {
    try {
        const response = await api.put(`/empresa-selos/${seloId}/solicitar-renovacao`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao solicitar renovação para o selo ${seloId}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Associa um novo tipo de selo a uma empresa.
 */
export const associarSeloAEmpresa = async (idEmpresa, dadosAssociacao) => {
    try {
        const response = await api.post(`/empresas/${idEmpresa}/selos`, dadosAssociacao);
        return response.data;
    } catch (error) {
        console.error(`Erro ao associar selo à empresa ${idEmpresa}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Permite que um usuário empresa solicite um selo.
 */
export const solicitarSelo = async (dadosSolicitacao) => {
    try {
        const response = await api.post('/selos/solicitar', dadosSolicitacao);
        return response.data;
    } catch (error) {
        console.error(`Erro ao solicitar selo:`, error.response?.data || error.message);
        throw error;
    }
};