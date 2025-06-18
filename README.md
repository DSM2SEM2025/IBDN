# 🏢 Projeto IBDN - Plataforma de Certificação e Gestão de Empresas

<div align="center">

![IBDN Logo](https://ibdn.org.br/wp-content/themes/ibdn-theme/assets/images/logo-ibdn.svg)

**Sistema completo para gerenciamento de empresas, certificações e usuários**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação-e-execução)
- [Estrutura](#-estrutura-do-projeto)
- [API Docs](#-documentação-da-api)
- [Scripts](#-scripts-disponíveis)
- [Roadmap](#-próximos-passos)

---

## ✨ Visão Geral

A **plataforma IBDN** é um sistema web completo que integra **frontend React** e **backend FastAPI** para o gerenciamento de certificações empresariais. A solução oferece uma interface intuitiva para administração de empresas, usuários, selos de certificação e permissões de acesso.

### 👥 Perfis de Usuário

- **🔧 Administradores:** Aprovação de selos, gerenciamento de empresas e usuários
- **🏢 Usuários Empresariais:** Cadastro de empresas, solicitação de selos e acompanhamento

---

## 🚀 Funcionalidades

<table>
<tr>
<td width="50%">

### 🔒 **Autenticação & Segurança**
- ✅ Login com JWT
- ✅ Perfis com permissões específicas
- ✅ Hash de senhas seguro

### 🏢 **Gestão de Empresas**
- ✅ CRUD completo de empresas
- ✅ Cadastro de endereços
- ✅ Múltiplos ramos de atuação

</td>
<td width="50%">

### 👥 **Gestão de Usuários**
- ✅ CRUD de usuários
- ✅ Associação a perfis
- ✅ Controle de permissões

### 🏅 **Sistema de Selos**
- ✅ Catálogo de certificações
- ✅ Processo de solicitação
- ✅ Aprovação por administradores

</td>
</tr>
</table>

### 🔔 **Recursos Adicionais**
- **Notificações em tempo real**
- **Interface responsiva**
- **API RESTful documentada**
- **Gerenciamento de estado otimizado**

---

## 🛠️ Tecnologias Utilizadas

<div align="center">

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)

### Frontend
![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-B73BFE?style=flat-square&logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)
![Zustand](https://img.shields.io/badge/Zustand-FF6B6B?style=flat-square&logo=zustand&logoColor=white)

</div>

<details>
<summary><b>📦 Dependências Completas</b></summary>

#### Backend
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para Python
- **MySQL** - Banco de dados relacional
- **Uvicorn** - Servidor ASGI
- **Pydantic** - Validação de dados
- **Python-Jose** - Manipulação de JWT
- **Passlib** - Hash de senhas
- **Alembic** - Migrações de banco (opcional)

#### Frontend
- **React** - Biblioteca UI
- **Vite** - Build tool e dev server
- **Zustand** - Gerenciamento de estado
- **TailwindCSS** - Framework CSS
- **React Router** - Roteamento
- **Axios** - Cliente HTTP
- **JWT Decode** - Decodificação de tokens

</details>

---

## ✅ Pré-requisitos

Certifique-se de ter instalado:

```bash
Node.js (LTS) ≥ 16.x
Python ≥ 3.8
MySQL ≥ 8.0
Git
```

---

## 🚀 Instalação e Execução

### 1️⃣ Clone o Repositório

```bash
git clone https://github.com/seu-usuario/projeto-ibdn.git
cd projeto-ibdn
```

### 2️⃣ Configuração do Backend

<details>
<summary><b>🔧 Configurar API (FastAPI)</b></summary>

#### Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate   # Windows
```

#### Variáveis de Ambiente
Crie o arquivo `.env` na raiz:

```env
# Database
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ibdn_db

# Security
SECRET_KEY=sua-chave-muito-secreta-aqui
ALLOWED_ORIGINS=http://localhost:5173

# Admin Default
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=senha_forte_123
```

#### Instalação e Execução
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

✅ **API disponível em:** http://localhost:8000

</details>

### 3️⃣ Configuração do Frontend

<details>
<summary><b>🖥️ Configurar Interface (React)</b></summary>

#### Navegue para o diretório
```bash
cd front_ibdn
```

#### Variáveis de Ambiente
Crie o arquivo `.env`:

```env
VITE_API_URL=http://localhost:8000
```

#### Instalação e Execução
```bash
npm install
# ou
yarn install

npm run dev
# ou
yarn dev
```

✅ **App disponível em:** http://localhost:5173

</details>

---

## 📁 Estrutura do Projeto

<div align="center">

```
projeto-ibdn/
├── 📂 app/                 # Backend (FastAPI)
│   ├── 📁 controllers/     # Lógica de negócio
│   ├── 📁 database/        # Config do banco
│   ├── 📁 models/          # Modelos de dados
│   ├── 📁 repository/      # Acesso aos dados
│   ├── 📁 routers/         # Endpoints da API
│   ├── 📁 security/        # Autenticação
│   └── 📁 service/         # Serviços auxiliares
│
├── 📂 front_ibdn/          # Frontend (React)
│   ├── 📁 src/
│   │   ├── 📁 components/  # Componentes reutilizáveis
│   │   ├── 📁 pages/       # Páginas da aplicação
│   │   ├── 📁 services/    # Comunicação com API
│   │   ├── 📁 store/       # Estado global (Zustand)
│   │   ├── 📄 App.jsx      # Rotas principais
│   │   └── 📄 main.jsx     # Ponto de entrada
│   │
│   ├── 📄 package.json
│   └── 📄 vite.config.js
│
├── 📄 requirements.txt     # Deps do Python
├── 📄 .env.example        # Exemplo de variáveis
└── 📄 README.md           # Este arquivo
```

</div>

---

## 📜 Documentação da API

Após iniciar o backend, acesse a documentação interativa:

<div align="center">

| Documentação | URL | Descrição |
|:---:|:---:|:---|
| 📚 **Swagger UI** | http://localhost:8000/docs | Interface interativa completa |
| 📖 **ReDoc** | http://localhost:8000/redoc | Documentação alternativa |

</div>

---

## 🧪 Scripts Disponíveis

### Frontend Commands

```bash
npm run dev      # 🚀 Servidor de desenvolvimento
npm run build    # 📦 Build para produção
npm run preview  # 👀 Visualizar build
npm run lint     # 🔍 Análise de código
```

### Backend Commands

```bash
uvicorn main:app --reload    # 🔄 Servidor com auto-reload
uvicorn main:app --port 8080 # 🌐 Servidor em porta específica
```

---

## 🧭 Próximos Passos

### 🔜 Roadmap

- [ ] **🧪 Testes Automatizados**
  - Pytest para backend
  - Vitest para frontend
  - Cobertura de código

- [ ] **🚀 Deploy & DevOps**
  - Containerização com Docker
  - CI/CD com GitHub Actions
  - Deploy em cloud (Heroku/Vercel)

- [ ] **📈 Monitoramento**
  - Logs estruturados
  - Métricas de performance
  - Alertas de sistema

- [ ] **🔒 Melhorias de Segurança**
  - Rate limiting
  - Validação avançada
  - Auditoria de ações

---

<div align="center">


⭐ **Se este projeto foi útil para você, considere dar uma estrela!**

</div>
