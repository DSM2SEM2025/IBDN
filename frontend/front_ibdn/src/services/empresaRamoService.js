import api from './api';

/**
 * Busca a lista de ramos associados a uma empresa específica.
 * @param {number} idEmpresa - O ID da empresa.
 * @returns {Promise<Array>} Uma lista de ramos.
 */
export const getRamosPorEmpresa = async (idEmpresa) => {
    try {
        const response = await api.get(`/${idEmpresa}/ramos/`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao buscar ramos para a empresa ${idEmpresa}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Atrela uma lista de ramos a uma empresa.
 * @param {number} idEmpresa - O ID da empresa.
 * @param {Array<number>} idsRamo - Um array com os IDs dos ramos a serem atrelados.
 * @returns {Promise<Object>} A resposta da API.
 */
export const atrelarRamosAEmpresa = async (idEmpresa, idsRamo) => {
    try {
        const response = await api.post(`/${idEmpresa}/ramos/`, { ids_ramo: idsRamo });
        return response.data;
    } catch (error) {
        console.error(`Erro ao atrelar ramos à empresa ${idEmpresa}:`, error.response?.data || error.message);
        throw error;
    }
};

/**
 * Remove a associação entre uma empresa e um ramo.
 * @param {number} idEmpresa - O ID da empresa.
 * @param {number} idRamo - O ID do ramo a ser desassociado.
 * @returns {Promise<void>}
 */
export const deleteAssociacao = async (idEmpresa, idRamo) => {
    try {
        const response = await api.delete(`/${idEmpresa}/ramos/${idRamo}/`);
        return response.data;
    } catch (error) {
        console.error(`Erro ao deletar associação do ramo ${idRamo} da empresa ${idEmpresa}:`, error.response?.data || error.message);
        throw error;
    }
};
