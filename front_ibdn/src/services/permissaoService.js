// src/services/permissaoService.js — Mock
import { getCollection, setCollection, delay } from '../data/mockStore';

const generateId = () => `perm-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`;

export const listarPermissoes = async () => {
  await delay();
  return getCollection('permissoes');
};

export const criarPermissao = async (dadosPermissao) => {
  await delay();
  const permissoes = getCollection('permissoes');
  const nova = { ...dadosPermissao, id: generateId() };
  setCollection('permissoes', [...permissoes, nova]);
  return nova;
};

export const atualizarPermissao = async (permissaoId, dadosAtualizacao) => {
  await delay();
  let permissoes = getCollection('permissoes');
  let atualizada = null;
  permissoes = permissoes.map((p) => {
    if (p.id === permissaoId) {
      atualizada = { ...p, ...dadosAtualizacao };
      return atualizada;
    }
    return p;
  });
  if (!atualizada) throw { response: { data: { detail: 'Permissão não encontrada.' } } };
  setCollection('permissoes', permissoes);
  return atualizada;
};

export const deletarPermissao = async (permissaoId) => {
  await delay();
  const permissoes = getCollection('permissoes');
  setCollection('permissoes', permissoes.filter((p) => p.id !== permissaoId));
  return { message: 'Permissão excluída com sucesso.' };
};