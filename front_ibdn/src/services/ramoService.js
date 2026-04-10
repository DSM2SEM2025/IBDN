// src/services/ramoService.js — Mock
import { getCollection, setCollection, nextId, delay } from '../data/mockStore';

export const listarRamos = async () => {
  await delay();
  return getCollection('ramos');
};

export const criarRamo = async (dadosRamo) => {
  await delay();
  const ramos = getCollection('ramos');
  const novoRamo = { ...dadosRamo, id: nextId('ramos') };
  setCollection('ramos', [...ramos, novoRamo]);
  return novoRamo;
};

export const atualizarRamo = async (ramoId, dadosAtualizacao) => {
  await delay();
  let ramos = getCollection('ramos');
  let atualizado = null;
  ramos = ramos.map((r) => {
    if (r.id === Number(ramoId)) {
      atualizado = { ...r, ...dadosAtualizacao };
      return atualizado;
    }
    return r;
  });
  if (!atualizado) throw { response: { data: { detail: 'Ramo não encontrado.' } } };
  setCollection('ramos', ramos);
  return atualizado;
};

export const deletarRamo = async (ramoId) => {
  await delay();
  const ramos = getCollection('ramos');
  setCollection('ramos', ramos.filter((r) => r.id !== Number(ramoId)));
  return { message: 'Ramo excluído com sucesso.' };
};
