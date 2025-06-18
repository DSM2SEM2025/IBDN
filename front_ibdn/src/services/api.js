import axios from 'axios';
import useAuthStore from '../store/authStore';

const api = axios.create({
    // IMPORTANTE: Substitua pela URL real do seu backend
    baseURL: 'http://localhost:8000',
});

// Interceptor para adicionar o token de autenticação a cada requisição
api.interceptors.request.use(
    (config) => {
        // Pega o token diretamente do estado da store do Zustand
        const token = useAuthStore.getState().token;
        if (token) {
            // Se o token existir, adiciona-o ao cabeçalho de autorização
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        // Em caso de erro na configuração da requisição, rejeita a promise
        return Promise.reject(error);
    }
);

export default api;
