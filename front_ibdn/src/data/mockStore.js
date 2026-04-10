// src/data/mockStore.js
// Store in-memory para a demo — sem localStorage, reseta a cada reload

import * as mockData from './mockData';

// Clona os dados iniciais para evitar mutação do módulo original
const deepClone = (obj) => JSON.parse(JSON.stringify(obj));

// ─── Estado in-memory ──────────────────────────────────
let store = {};

const resetStore = () => {
  store = {
    empresas: deepClone(mockData.empresas),
    enderecos: deepClone(mockData.enderecos),
    ramos: deepClone(mockData.ramos),
    empresa_ramos: deepClone(mockData.empresa_ramos),
    tipos_selo: deepClone(mockData.tipos_selo),
    selos: deepClone(mockData.selos),
    permissoes: deepClone(mockData.permissoes),
    perfis: deepClone(mockData.perfis),
    usuarios: deepClone(mockData.usuarios),
    notificacoes: deepClone(mockData.notificacoes),
  };
};

// Inicializa
resetStore();

// ─── API do Store ──────────────────────────────────────

export const getCollection = (name) => store[name] || [];

export const setCollection = (name, data) => {
  store[name] = data;
};

export const getById = (collection, id) => {
  const items = getCollection(collection);
  return items.find((item) => item.id === id || item.id === Number(id)) || null;
};

export const nextId = (collection) => {
  const items = getCollection(collection);
  if (items.length === 0) return 1;
  const maxId = Math.max(...items.map((i) => (typeof i.id === 'number' ? i.id : 0)));
  return maxId + 1;
};

// Simula ~200ms de latência de rede
export const delay = (ms = 200) => new Promise((resolve) => setTimeout(resolve, ms));

export { resetStore };
