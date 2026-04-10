// src/data/mockData.js
// Dados estáticos para a demo funcional do IBDN (sem backend)

// ─── Permissões ────────────────────────────────────────
export const permissoes = [
  { id: "perm-001", nome: "admin" },
  { id: "perm-002", nome: "admin_master" },
  { id: "perm-003", nome: "empresa" },
  { id: "perm-004", nome: "visualizar_relatorios" },
  { id: "perm-005", nome: "gerir_selos" },
  { id: "perm-006", nome: "gerir_usuarios" },
];

// ─── Perfis ────────────────────────────────────────────
export const perfis = [
  {
    id: "perfil-001",
    nome: "Administrador",
    permissoes: [
      { id: "perm-001", nome: "admin" },
      { id: "perm-002", nome: "admin_master" },
      { id: "perm-004", nome: "visualizar_relatorios" },
      { id: "perm-005", nome: "gerir_selos" },
      { id: "perm-006", nome: "gerir_usuarios" },
    ],
  },
  {
    id: "perfil-002",
    nome: "Empresa",
    permissoes: [
      { id: "perm-003", nome: "empresa" },
      { id: "perm-004", nome: "visualizar_relatorios" },
    ],
  },
];

// ─── Usuários ──────────────────────────────────────────
export const usuarios = [
  {
    id: "user-001",
    nome: "Administrador IBDN",
    email: "admin@ibdn.com",
    ativo: true,
    twofactor: false,
    perfil: {
      id: "perfil-001",
      nome: "Administrador",
      permissoes: [
        { id: "perm-001", nome: "admin" },
        { id: "perm-002", nome: "admin_master" },
        { id: "perm-004", nome: "visualizar_relatorios" },
        { id: "perm-005", nome: "gerir_selos" },
        { id: "perm-006", nome: "gerir_usuarios" },
      ],
    },
  },
  {
    id: "user-002",
    nome: "Maria Silva",
    email: "empresa@ibdn.com",
    ativo: true,
    twofactor: false,
    perfil: {
      id: "perfil-002",
      nome: "Empresa",
      permissoes: [
        { id: "perm-003", nome: "empresa" },
        { id: "perm-004", nome: "visualizar_relatorios" },
      ],
    },
  },
  {
    id: "user-003",
    nome: "João Santos",
    email: "joao@ecogreen.com",
    ativo: true,
    twofactor: true,
    perfil: {
      id: "perfil-002",
      nome: "Empresa",
      permissoes: [
        { id: "perm-003", nome: "empresa" },
        { id: "perm-004", nome: "visualizar_relatorios" },
      ],
    },
  },
  {
    id: "user-004",
    nome: "Ana Oliveira",
    email: "ana@sustentabilidade.org",
    ativo: false,
    twofactor: false,
    perfil: {
      id: "perfil-002",
      nome: "Empresa",
      permissoes: [
        { id: "perm-003", nome: "empresa" },
        { id: "perm-004", nome: "visualizar_relatorios" },
      ],
    },
  },
];

// ─── Ramos ─────────────────────────────────────────────
export const ramos = [
  { id: 1, nome: "Agronegócio", descricao: "Atividades agroindustriais e pecuárias sustentáveis" },
  { id: 2, nome: "Tecnologia", descricao: "Empresas de TI, software e hardware verde" },
  { id: 3, nome: "Construção Civil", descricao: "Edificações e infraestrutura com selo ambiental" },
  { id: 4, nome: "Energia Renovável", descricao: "Geração e distribuição de energia limpa" },
  { id: 5, nome: "Logística", descricao: "Transporte e cadeia de suprimentos sustentável" },
];

// ─── Empresas ──────────────────────────────────────────
export const empresas = [
  {
    id: 1,
    cnpj: "12.345.678/0001-90",
    razao_social: "EcoGreen Soluções Ambientais Ltda",
    nome_fantasia: "EcoGreen",
    usuario_id: "user-002",
    telefone: "(11) 98765-4321",
    responsavel: "Maria Silva",
    cargo_responsavel: "Diretora de Sustentabilidade",
    site: "https://ecogreen.com.br",
    data_cadastro: "2024-03-15",
    ativo: true,
  },
  {
    id: 2,
    cnpj: "98.765.432/0001-10",
    razao_social: "Sustenta Mais Engenharia S.A.",
    nome_fantasia: "Sustenta+",
    usuario_id: "user-003",
    telefone: "(21) 99876-5432",
    responsavel: "João Santos",
    cargo_responsavel: "CEO",
    site: "https://sustentamais.eng.br",
    data_cadastro: "2024-06-22",
    ativo: true,
  },
  {
    id: 3,
    cnpj: "55.123.789/0001-55",
    razao_social: "Reciclagem Total Ind. Com. Ltda",
    nome_fantasia: "ReciTotal",
    usuario_id: "user-004",
    telefone: "(31) 3456-7890",
    responsavel: "Ana Oliveira",
    cargo_responsavel: "Gerente Ambiental",
    site: "https://recitotal.com",
    data_cadastro: "2025-01-10",
    ativo: false,
  },
];

// ─── Endereços ─────────────────────────────────────────
export const enderecos = [
  {
    id: 1,
    id_empresa: 1,
    logradouro: "Rua das Palmeiras",
    numero: "450",
    bairro: "Jardim Botânico",
    cep: "01310-100",
    cidade: "São Paulo",
    uf: "SP",
    complemento: "Sala 201",
  },
  {
    id: 2,
    id_empresa: 2,
    logradouro: "Av. Atlântica",
    numero: "1200",
    bairro: "Copacabana",
    cep: "22021-000",
    cidade: "Rio de Janeiro",
    uf: "RJ",
    complemento: "Bloco B, 15º andar",
  },
  {
    id: 3,
    id_empresa: 3,
    logradouro: "Rua Serra do Curral",
    numero: "88",
    bairro: "Funcionários",
    cep: "30130-000",
    cidade: "Belo Horizonte",
    uf: "MG",
    complemento: "",
  },
];

// ─── Associação Empresa ↔ Ramo ─────────────────────────
export const empresa_ramos = [
  { id_empresa: 1, id_ramo: 1 },
  { id_empresa: 1, id_ramo: 4 },
  { id_empresa: 2, id_ramo: 3 },
  { id_empresa: 2, id_ramo: 4 },
  { id_empresa: 3, id_ramo: 1 },
  { id_empresa: 3, id_ramo: 5 },
];

// ─── Tipos de Selo (Catálogo) ──────────────────────────
export const tipos_selo = [
  { id: 1, nome: "Selo Verde Premium", descricao: "Certificação máxima de conformidade ambiental para empresas líderes em sustentabilidade.", sigla: "SVP" },
  { id: 2, nome: "Selo Carbono Neutro", descricao: "Certificação para empresas que compensam 100% de suas emissões de carbono.", sigla: "SCN" },
  { id: 3, nome: "Selo Gestão Hídrica", descricao: "Certificação de gestão responsável de recursos hídricos e tratamento de efluentes.", sigla: "SGH" },
  { id: 4, nome: "Selo Economia Circular", descricao: "Certificação para empresas com práticas de reutilização e reciclagem integradas.", sigla: "SEC" },
];

// ─── Selos Concedidos/Solicitados ──────────────────────
export const selos = [
  {
    id: 1,
    id_empresa: 1,
    id_selo: 1,
    status: "Aprovado",
    data_emissao: "2024-04-01",
    data_expiracao: "2026-04-01",
    codigo_selo: "SVP-2024-001",
    nome_selo: "Selo Verde Premium",
    sigla_selo: "SVP",
    razao_social: "EcoGreen Soluções Ambientais Ltda",
  },
  {
    id: 2,
    id_empresa: 1,
    id_selo: 2,
    status: "Aprovado",
    data_emissao: "2024-07-15",
    data_expiracao: "2026-07-15",
    codigo_selo: "SCN-2024-001",
    nome_selo: "Selo Carbono Neutro",
    sigla_selo: "SCN",
    razao_social: "EcoGreen Soluções Ambientais Ltda",
  },
  {
    id: 3,
    id_empresa: 2,
    id_selo: 3,
    status: "Pendente",
    data_emissao: null,
    data_expiracao: null,
    codigo_selo: null,
    nome_selo: "Selo Gestão Hídrica",
    sigla_selo: "SGH",
    razao_social: "Sustenta Mais Engenharia S.A.",
  },
  {
    id: 4,
    id_empresa: 2,
    id_selo: 1,
    status: "Aprovado",
    data_emissao: "2024-09-01",
    data_expiracao: "2026-09-01",
    codigo_selo: "SVP-2024-002",
    nome_selo: "Selo Verde Premium",
    sigla_selo: "SVP",
    razao_social: "Sustenta Mais Engenharia S.A.",
  },
  {
    id: 5,
    id_empresa: 1,
    id_selo: 4,
    status: "Pendente",
    data_emissao: null,
    data_expiracao: null,
    codigo_selo: null,
    nome_selo: "Selo Economia Circular",
    sigla_selo: "SEC",
    razao_social: "EcoGreen Soluções Ambientais Ltda",
  },
];

// ─── Notificações ──────────────────────────────────────
export const notificacoes = [
  {
    id: 1,
    id_empresa: 1,
    mensagem: "Seu Selo Verde Premium foi aprovado com sucesso! Parabéns pela conquista.",
    tipo: "sucesso",
    lida: false,
    data_envio: "2024-04-01T10:30:00",
  },
  {
    id: 2,
    id_empresa: 1,
    mensagem: "Lembrete: O Selo Carbono Neutro expira em 90 dias. Considere solicitar a renovação.",
    tipo: "aviso",
    lida: false,
    data_envio: "2024-06-15T14:00:00",
  },
  {
    id: 3,
    id_empresa: 1,
    mensagem: "Nova funcionalidade disponível: agora você pode acompanhar o status dos selos em tempo real.",
    tipo: "info",
    lida: true,
    data_envio: "2024-05-20T09:00:00",
  },
  {
    id: 4,
    id_empresa: 2,
    mensagem: "Sua solicitação do Selo Gestão Hídrica foi recebida e está em análise.",
    tipo: "info",
    lida: false,
    data_envio: "2024-08-10T11:15:00",
  },
];
