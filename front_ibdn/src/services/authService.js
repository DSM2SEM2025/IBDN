import api from './api';

/**
 * Autentica o usuário no backend real.
 * Endpoint: POST /login
 * Body: { email, senha }
 * Retorna: { access_token, message } + dados do usuário extraídos do JWT
 */
export const login = async (email, senha) => {
  const response = await api.post('/login', { email, senha });
  const { access_token, message } = response.data;

  // Decodifica o payload do JWT para obter dados do usuário (sem verificação de assinatura no cliente)
  const payloadBase64 = access_token.split('.')[1];
  const payload = JSON.parse(atob(payloadBase64));

  const user = {
    id: payload.sub,
    email: payload.email ?? email,
    empresa_id: payload.empresa_id ?? null,
    permissoes: payload.permissoes ?? [],
  };

  return { access_token, user };
};
