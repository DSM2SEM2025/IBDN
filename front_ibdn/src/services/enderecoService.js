// src/services/enderecoService.js — Mock
import { getCollection, setCollection, nextId, delay } from '../data/mockStore';

export const listarEnderecosDaEmpresa = async (idEmpresa) => {
  await delay();
  return getCollection('enderecos').filter((e) => e.id_empresa === Number(idEmpresa));
};

export const getEndereco = async (idEmpresa) => {
  await delay();
  const enderecos = getCollection('enderecos').filter((e) => e.id_empresa === Number(idEmpresa));
  return enderecos.length > 0 ? enderecos[0] : null;
};

export const criarEndereco = async (idEmpresa, dadosEndereco) => {
  await delay();
  const enderecos = getCollection('enderecos');
  const novoEndereco = {
    ...dadosEndereco,
    id: nextId('enderecos'),
    id_empresa: Number(idEmpresa),
  };
  setCollection('enderecos', [...enderecos, novoEndereco]);
  return novoEndereco;
};

export const atualizarEndereco = async (idEmpresa, dadosAtualizacao) => {
  await delay();
  let enderecos = getCollection('enderecos');
  let atualizado = null;
  enderecos = enderecos.map((e) => {
    if (e.id_empresa === Number(idEmpresa)) {
      atualizado = { ...e, ...dadosAtualizacao };
      return atualizado;
    }
    return e;
  });
  if (!atualizado) throw { response: { data: { detail: 'Endereço não encontrado.' } } };
  setCollection('enderecos', enderecos);
  return atualizado;
};

export const deletarEndereco = async (idEmpresa) => {
  await delay();
  const enderecos = getCollection('enderecos');
  setCollection('enderecos', enderecos.filter((e) => e.id_empresa !== Number(idEmpresa)));
  return { message: 'Endereço excluído com sucesso.' };
};