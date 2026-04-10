// src/services/empresaService.js — Mock
import { getCollection, setCollection, getById, nextId, delay } from '../data/mockStore';

export const listarEmpresas = async () => {
  await delay();
  return getCollection('empresas');
};

export const buscarEmpresaPorId = async (empresaId) => {
  await delay();
  const empresa = getById('empresas', empresaId);
  if (!empresa) throw { response: { data: { detail: 'Empresa não encontrada.' } } };
  return empresa;
};

export const adicionarEmpresa = async (dadosEmpresa) => {
  await delay();
  const empresas = getCollection('empresas');
  const novaEmpresa = {
    ...dadosEmpresa,
    id: nextId('empresas'),
    data_cadastro: new Date().toISOString().split('T')[0],
    ativo: true,
  };
  setCollection('empresas', [...empresas, novaEmpresa]);
  return novaEmpresa;
};

export const atualizarEmpresa = async (empresaId, dadosAtualizacao) => {
  await delay();
  let empresas = getCollection('empresas');
  let atualizada = null;
  empresas = empresas.map((e) => {
    if (e.id === Number(empresaId) || e.id === empresaId) {
      atualizada = { ...e, ...dadosAtualizacao };
      return atualizada;
    }
    return e;
  });
  if (!atualizada) throw { response: { data: { detail: 'Empresa não encontrada.' } } };
  setCollection('empresas', empresas);
  return atualizada;
};

export const excluirEmpresa = async (empresaId) => {
  await delay();
  const empresas = getCollection('empresas');
  setCollection('empresas', empresas.filter((e) => e.id !== Number(empresaId) && e.id !== empresaId));
  return { message: 'Empresa excluída com sucesso.' };
};