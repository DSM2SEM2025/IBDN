// src/services/tipoSeloService.js
import api from './api';

export const listarTiposSelo = async () => {
    try {
        // CORREÇÃO: A rota correta é /selos-catalogo/ conforme o backend
        const response = await api.get('/selos-catalogo/');
        return response.data;
    } catch (error) {
        console.error('Erro ao listar tipos de selo:', error.response?.data || error.message);
        throw error;
    }
};

export const criarTipoSelo = async (dados) => {
    try {
        // CORREÇÃO: A rota correta é /selos-catalogo/
        const response = await api.post('/selos-catalogo/', dados);
        return response.data;
    } catch (error) {
        console.error('Erro ao criar tipo de selo:', error.response?.data || error.message);
        throw error;
    }
};

export const atualizarTipoSelo = async (id, dados) => {
    try {
        // Esta rota não foi implementada no seu backend, mas se fosse, o caminho seria este:
        const response = await api.put(`/selos-catalogo/${id}`, dados);
        return response.data;
    } catch (error) {
        console.error(`Erro ao atualizar tipo de selo ${id}:`, error.response?.data || error.message);
        throw error;
    }
};

export const deletarTipoSelo = async (id) => {
    try {
        // Esta rota não foi implementada no seu backend, mas se fosse, o caminho seria este:
        const response = await api.delete(`/selos-catalogo/${id}`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao deletar tipo de selo ${id}:`, error.response?.data || error.message);
        throw error;
    }
};