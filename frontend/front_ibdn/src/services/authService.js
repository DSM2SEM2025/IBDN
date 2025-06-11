import api from './api'; // Importa a instância configurada do Axios

/**
 * Envia as credenciais do usuário para o endpoint de login da API.
 * @param {string} email - O email do usuário.
 * @param {string} senha - A senha do usuário.
 * @returns {Promise<Object>} A resposta da API, contendo o token de acesso.
 */
export const login = async (email, senha) => {
    try {
        // Realiza a chamada POST para o endpoint /login
        // O corpo da requisição é um objeto com email e senha, como esperado pela API
        const response = await api.post('/login', {
            email,
            senha,
        });
        // Retorna os dados da resposta em caso de sucesso
        return response.data;
    } catch (error) {
        // Em caso de erro, loga o erro no console e relança para ser tratado no componente
        console.error('Erro na autenticação:', error.response?.data || error.message);
        throw error;
    }
};
