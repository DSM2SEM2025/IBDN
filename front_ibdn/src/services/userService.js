// src/services/userService.js — Mock (registro desabilitado na demo)
import { delay } from '../data/mockStore';

export const register = async (dadosUsuario) => {
  await delay(400);
  // Na demo, o registro não cria conta funcional — apenas simula sucesso
  return { message: 'Conta criada com sucesso! Use as credenciais de demo para acessar.' };
};