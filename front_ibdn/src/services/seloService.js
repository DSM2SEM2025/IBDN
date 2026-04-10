// src/services/seloService.js — Mock
import { getCollection, setCollection, nextId, delay } from '../data/mockStore';

export const listarTodosSelos = async () => {
  await delay();
  // SelosPage espera { dados: [...] }
  return { dados: getCollection('selos') };
};

export const getSelosByEmpresa = async (empresaId) => {
  await delay();
  return getCollection('selos').filter((s) => s.id_empresa === Number(empresaId));
};

export const getSolicitacoesSelo = async () => {
  await delay();
  return getCollection('selos').filter(
    (s) => s.status === 'Pendente' || s.status === 'Em Renovação'
  );
};

export const aprovarSelo = async (seloId) => {
  await delay();
  let selos = getCollection('selos');
  const tiposSelo = getCollection('tipos_selo');
  selos = selos.map((s) => {
    if (s.id === Number(seloId)) {
      const tipo = tiposSelo.find((t) => t.id === s.id_selo);
      const hoje = new Date();
      const expiracao = new Date(hoje);
      expiracao.setFullYear(expiracao.getFullYear() + 2);
      return {
        ...s,
        status: 'Aprovado',
        data_emissao: hoje.toISOString().split('T')[0],
        data_expiracao: expiracao.toISOString().split('T')[0],
        codigo_selo: `${tipo?.sigla || 'SEL'}-${hoje.getFullYear()}-${String(s.id).padStart(3, '0')}`,
      };
    }
    return s;
  });
  setCollection('selos', selos);
  return { message: 'Selo aprovado com sucesso.' };
};

export const recusarSelo = async (seloId) => {
  await delay();
  let selos = getCollection('selos');
  selos = selos.map((s) => {
    if (s.id === Number(seloId)) {
      return { ...s, status: 'Recusado' };
    }
    return s;
  });
  setCollection('selos', selos);
  return { message: 'Selo recusado.' };
};

export const solicitarRenovacaoSelo = async (seloId) => {
  await delay();
  let selos = getCollection('selos');
  selos = selos.map((s) => {
    if (s.id === Number(seloId)) {
      return { ...s, status: 'Em Renovação' };
    }
    return s;
  });
  setCollection('selos', selos);
  return { message: 'Renovação solicitada.' };
};

export const associarSeloAEmpresa = async (idEmpresa, dadosAssociacao) => {
  await delay();
  const selos = getCollection('selos');
  const tiposSelo = getCollection('tipos_selo');
  const empresas = getCollection('empresas');
  const tipo = tiposSelo.find((t) => t.id === Number(dadosAssociacao.id_selo));
  const empresa = empresas.find((e) => e.id === Number(idEmpresa));

  const novoSelo = {
    id: nextId('selos'),
    id_empresa: Number(idEmpresa),
    id_selo: Number(dadosAssociacao.id_selo),
    status: 'Pendente',
    data_emissao: null,
    data_expiracao: null,
    codigo_selo: null,
    nome_selo: tipo?.nome || 'Selo',
    sigla_selo: tipo?.sigla || 'N/A',
    razao_social: empresa?.razao_social || 'N/A',
  };
  setCollection('selos', [...selos, novoSelo]);
  return novoSelo;
};

export const solicitarSelo = async (dadosSolicitacao) => {
  await delay();
  const selos = getCollection('selos');
  const tiposSelo = getCollection('tipos_selo');
  const tipo = tiposSelo.find((t) => t.id === Number(dadosSolicitacao.id_selo));

  // Pega o empresa_id do primeiro selo da empresa ou usa 1 como fallback
  const novoSelo = {
    id: nextId('selos'),
    id_empresa: dadosSolicitacao.id_empresa || 1,
    id_selo: Number(dadosSolicitacao.id_selo),
    status: 'Pendente',
    data_emissao: null,
    data_expiracao: null,
    codigo_selo: null,
    nome_selo: tipo?.nome || 'Selo',
    sigla_selo: tipo?.sigla || 'N/A',
    razao_social: 'Empresa Solicitante',
  };
  setCollection('selos', [...selos, novoSelo]);
  return novoSelo;
};