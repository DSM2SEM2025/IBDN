// src/services/notificacaoService.js — Mock
import { getCollection, setCollection, nextId, delay } from '../data/mockStore';

export const listarNotificacoesEmpresa = async (idEmpresa, lida = null) => {
  await delay();
  let notificacoes = getCollection('notificacoes').filter(
    (n) => n.id_empresa === Number(idEmpresa)
  );
  if (lida !== null) {
    notificacoes = notificacoes.filter((n) => n.lida === lida);
  }
  return notificacoes;
};

export const criarNotificacao = async (idEmpresa, dadosNotificacao) => {
  await delay();
  const notificacoes = getCollection('notificacoes');
  const nova = {
    ...dadosNotificacao,
    id: nextId('notificacoes'),
    id_empresa: Number(idEmpresa),
    lida: false,
    data_envio: new Date().toISOString(),
  };
  setCollection('notificacoes', [...notificacoes, nova]);
  return nova;
};

export const atualizarNotificacao = async (idNotificacao, dadosAtualizacao) => {
  await delay();
  let notificacoes = getCollection('notificacoes');
  let atualizada = null;
  notificacoes = notificacoes.map((n) => {
    if (n.id === Number(idNotificacao)) {
      atualizada = { ...n, ...dadosAtualizacao };
      return atualizada;
    }
    return n;
  });
  if (!atualizada) throw { response: { data: { detail: 'Notificação não encontrada.' } } };
  setCollection('notificacoes', notificacoes);
  return atualizada;
};

export const deletarNotificacao = async (idNotificacao) => {
  await delay();
  const notificacoes = getCollection('notificacoes');
  setCollection('notificacoes', notificacoes.filter((n) => n.id !== Number(idNotificacao)));
  return { message: 'Notificação excluída com sucesso.' };
};
