// src/services/authService.js
// Mock de autenticação — dois perfis pré-definidos

import { delay } from '../data/mockStore';

const MOCK_USERS = {
  'admin@ibdn.com': {
    senha: '12345678',
    user: {
      id: 'user-001',
      email: 'admin@ibdn.com',
      empresa_id: null,
      permissoes: ['admin', 'admin_master', 'visualizar_relatorios', 'gerir_selos', 'gerir_usuarios'],
    },
  },
  'empresa@ibdn.com': {
    senha: '12345678',
    user: {
      id: 'user-002',
      email: 'empresa@ibdn.com',
      empresa_id: 1,
      permissoes: ['empresa', 'visualizar_relatorios'],
    },
  },
};

export const login = async (email, senha) => {
  await delay(400);

  const entry = MOCK_USERS[email];
  if (!entry || entry.senha !== senha) {
    throw { response: { data: { detail: 'Credenciais inválidas.' } } };
  }

  // Retorna no mesmo formato que o LoginPage espera
  return { access_token: 'demo-token', user: entry.user };
};
