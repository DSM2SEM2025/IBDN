// src/services/tipoSeloService.js — Mock
import { getCollection, setCollection, nextId, delay } from '../data/mockStore';

export const listarTiposSelo = async () => {
  await delay();
  return getCollection('tipos_selo');
};

export const criarTipoSelo = async (dados) => {
  await delay();
  const tipos = getCollection('tipos_selo');
  const novoTipo = { ...dados, id: nextId('tipos_selo') };
  setCollection('tipos_selo', [...tipos, novoTipo]);
  return novoTipo;
};

export const atualizarTipoSelo = async (id, dados) => {
  await delay();
  let tipos = getCollection('tipos_selo');
  let atualizado = null;
  tipos = tipos.map((t) => {
    if (t.id === Number(id)) {
      atualizado = { ...t, ...dados };
      return atualizado;
    }
    return t;
  });
  if (!atualizado) throw { response: { data: { detail: 'Tipo de selo não encontrado.' } } };
  setCollection('tipos_selo', tipos);
  return atualizado;
};

export const deletarTipoSelo = async (id) => {
  await delay();
  const tipos = getCollection('tipos_selo');
  setCollection('tipos_selo', tipos.filter((t) => t.id !== Number(id)));
  return { message: 'Tipo de selo excluído com sucesso.' };
};