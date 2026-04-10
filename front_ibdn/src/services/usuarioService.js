// src/services/usuarioService.js — Mock
import { getCollection, setCollection, delay } from '../data/mockStore';

const generateId = () => `user-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`;

export const listarUsuarios = async () => {
  await delay();
  return getCollection('usuarios');
};

export const criarUsuario = async (dadosUsuario) => {
  await delay();
  const usuarios = getCollection('usuarios');
  const perfis = getCollection('perfis');

  // Resolve perfil_id para objeto perfil completo
  const perfil = dadosUsuario.perfil_id
    ? perfis.find((p) => p.id === dadosUsuario.perfil_id)
    : perfis.find((p) => p.nome === 'Empresa');

  const novoUsuario = {
    id: generateId(),
    nome: dadosUsuario.nome,
    email: dadosUsuario.email,
    ativo: dadosUsuario.ativo !== undefined ? dadosUsuario.ativo : true,
    twofactor: dadosUsuario.twofactor || false,
    perfil: perfil || null,
  };
  setCollection('usuarios', [...usuarios, novoUsuario]);
  return novoUsuario;
};

export const atualizarUsuario = async (usuarioId, dadosAtualizacao) => {
  await delay();
  let usuarios = getCollection('usuarios');
  const perfis = getCollection('perfis');
  let atualizado = null;

  usuarios = usuarios.map((u) => {
    if (u.id === usuarioId) {
      const perfil = dadosAtualizacao.perfil_id
        ? perfis.find((p) => p.id === dadosAtualizacao.perfil_id) || u.perfil
        : u.perfil;

      atualizado = { ...u, ...dadosAtualizacao, perfil };
      delete atualizado.perfil_id; // Remove campo auxiliar
      return atualizado;
    }
    return u;
  });
  if (!atualizado) throw { response: { data: { detail: 'Utilizador não encontrado.' } } };
  setCollection('usuarios', usuarios);
  return atualizado;
};

export const deletarUsuario = async (usuarioId) => {
  await delay();
  const usuarios = getCollection('usuarios');
  setCollection('usuarios', usuarios.filter((u) => u.id !== usuarioId));
  return { message: 'Utilizador excluído com sucesso.' };
};
