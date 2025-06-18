import api from './api';

/**
 * Envia os dados de um novo usuário para o endpoint de registro.
 * @param {Object} dadosUsuario - Os dados do novo usuário.
 * @param {string} dadosUsuario.nome - O nome completo do usuário.
 * @param {string} dadosUsuario.email - O email do usuário.
 * @param {string} dadosUsuario.senha - A senha do usuário.
 * @param {string} dadosUsuario.senha_confirmacao - A confirmação da senha.
 * @returns {Promise<Object>} A resposta da API.
 */
export const register = async (dadosUsuario) => {
    try {
        // A rota do backend é /usuario/register
        const response = await api.post('/usuario/register', dadosUsuario);
        return response.data;
    } catch (error) {
        // Relança o erro para ser tratado no componente que chamou a função
        console.error('Erro no registro:', error.response?.data || error.message);
        throw error.response?.data || error;
    }
};