// src/services/tipoSeloService.js
import api from './api';

export const listarTiposSelo = async () => {
    try {
        const response = await api.get('/tipos_selo/');
        return response.data;
    } catch (error) {
        console.error('Erro ao listar tipos de selo:', error.response?.data || error.message);
        throw error;
    }
};

export const criarTipoSelo = async (dados) => {
    try {
        const response = await api.post('/tipos_selo/', dados);
        return response.data;
    } catch (error) {
        console.error('Erro ao criar tipo de selo:', error.response?.data || error.message);
        throw error;
    }
};

export const atualizarTipoSelo = async (id, dados) => {
    try {
        const response = await api.put(`/tipos_selo/${id}`, dados);
        return response.data;
    } catch (error) {
        console.error(`Erro ao atualizar tipo de selo ${id}:`, error.response?.data || error.message);
        throw error;
    }
};

export const deletarTipoSelo = async (id) => {
    try {
        const response = await api.delete(`/tipos_selo/${id}`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao deletar tipo de selo ${id}:`, error.response?.data || error.message);
        throw error;
    }
};