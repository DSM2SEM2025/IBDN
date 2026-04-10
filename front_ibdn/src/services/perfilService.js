// src/services/perfilService.js — Mock
import { getCollection, setCollection, delay } from '../data/mockStore';

const generateId = () => `perfil-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`;

export const listarPerfis = async () => {
  await delay();
  return getCollection('perfis');
};

export const criarPerfil = async (dadosPerfil) => {
  await delay();
  const perfis = getCollection('perfis');
  const permissoes = getCollection('permissoes');

  // Resolve permissoes_ids para objetos completos
  const permissoesResolvidas = (dadosPerfil.permissoes_ids || [])
    .map((id) => permissoes.find((p) => p.id === id))
    .filter(Boolean);

  const novoPerfil = {
    id: generateId(),
    nome: dadosPerfil.nome,
    permissoes: permissoesResolvidas,
  };
  setCollection('perfis', [...perfis, novoPerfil]);
  return novoPerfil;
};

export const atualizarPerfil = async (perfilId, dadosAtualizacao) => {
  await delay();
  let perfis = getCollection('perfis');
  const permissoes = getCollection('permissoes');
  let atualizado = null;

  perfis = perfis.map((p) => {
    if (p.id === perfilId) {
      const permissoesResolvidas = dadosAtualizacao.permissoes_ids
        ? dadosAtualizacao.permissoes_ids.map((id) => permissoes.find((pm) => pm.id === id)).filter(Boolean)
        : p.permissoes;

      atualizado = {
        ...p,
        nome: dadosAtualizacao.nome || p.nome,
        permissoes: permissoesResolvidas,
      };
      return atualizado;
    }
    return p;
  });
  if (!atualizado) throw { response: { data: { detail: 'Perfil não encontrado.' } } };
  setCollection('perfis', perfis);
  return atualizado;
};

export const deletarPerfil = async (perfilId) => {
  await delay();
  const perfis = getCollection('perfis');
  setCollection('perfis', perfis.filter((p) => p.id !== perfilId));
  return { message: 'Perfil excluído com sucesso.' };
};

export const adicionarPermissaoAoPerfil = async (perfilId, permissaoId) => {
  await delay();
  let perfis = getCollection('perfis');
  const permissoes = getCollection('permissoes');
  const permissao = permissoes.find((p) => p.id === permissaoId);
  if (!permissao) throw { response: { data: { detail: 'Permissão não encontrada.' } } };

  perfis = perfis.map((p) => {
    if (p.id === perfilId && !p.permissoes.some((pm) => pm.id === permissaoId)) {
      return { ...p, permissoes: [...p.permissoes, permissao] };
    }
    return p;
  });
  setCollection('perfis', perfis);
  return perfis.find((p) => p.id === perfilId);
};

export const removerPermissaoDoPerfil = async (perfilId, permissaoId) => {
  await delay();
  let perfis = getCollection('perfis');
  perfis = perfis.map((p) => {
    if (p.id === perfilId) {
      return { ...p, permissoes: p.permissoes.filter((pm) => pm.id !== permissaoId) };
    }
    return p;
  });
  setCollection('perfis', perfis);
  return perfis.find((p) => p.id === perfilId);
};