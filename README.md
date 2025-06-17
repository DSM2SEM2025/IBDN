# 🛠️ Guia de Configuração e Execução do Projeto

Este guia descreve os passos necessários para configurar e executar o projeto em um ambiente de desenvolvimento local.

## 🏗️ Arquitetura do Projeto

O projeto utiliza uma arquitetura em camadas para separar as responsabilidades e garantir a organização do código:

* **`main.py` (Ponto de Entrada)**: Arquivo principal que inicializa a aplicação FastAPI, configura o CORS, e inclui todos os roteadores.
* **`routers/`**: Define os endpoints da API. Cada arquivo corresponde a um recurso específico (ex: `routes_empresa.py`, `ibdn_users_routes.py`) e delega a lógica para os *controllers*.
* **`controllers/`**: Contém a lógica de negócio da aplicação. Eles recebem as requisições dos roteadores, validam permissões, e orquestram as operações, interagindo com os *repositories* (ex: `controller_empresa.py`, `ibdn_users_controller.py`).
* **`repository/`**: Camada de acesso a dados. É responsável por toda a comunicação com o banco de dados, executando queries SQL (ex: `empresa_repository.py`, `ibdn_user_repository.py`).
* **`models/`**: Contém os modelos de dados Pydantic que definem a estrutura das requisições e respostas da API, garantindo a validação dos dados (ex: `empresas_model.py`, `ibdn_user_model.py`).
* **`security/`**: Inclui módulos para funcionalidades de segurança, como hashing de senhas com `passlib` e `bcrypt`.
* **`database/`**: Gerencia a configuração, conexão e criação das tabelas do banco de dados.

---

## ✅ Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados em sua máquina:

* **Python 3.8 ou superior**
* **MySQL Server**
* **Node.js (versão 18 ou superior)**
* **npm ou yarn**

---

## 🚀 Passos para Instalação

Siga os passos abaixo para colocar o projeto em funcionamento.

### 1. Clonar o Repositório

```bash
git clone https://github.com/DSM2SEM2025/IBDN.git
cd IBDN
```

### 2. Criar e Ativar um Ambiente Virtual

É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar no Windows
.\venv\Scripts\activate

# Ativar no macOS/Linux
source venv/bin/activate
```

### 3. Instalar as Dependências do Backend

Em seguida, instale todas as dependências com o pip:

```bash
pip install -r requirements.txt
```

### 4. Configurar o Banco de Dados

O projeto utiliza um script para criar o banco de dados e as tabelas automaticamente.

1. **Garanta que o seu serviço MySQL esteja em execução.**
2. O script tentará criar um banco de dados chamado `XE`, conforme indicado nos logs. Se você precisar de um nome diferente, ajuste-o no seu arquivo de configuração de ambiente.

### 5. Configurar as Variáveis de Ambiente

Crie um arquivo chamado `.env` na raiz do projeto. Ele armazenará as credenciais e chaves secretas de forma segura. Copie o conteúdo abaixo para o seu `.env` e substitua pelos seus valores.

```env
# Configuração do Banco de Dados
DB_HOST=localhost
DB_USER=seu_usuario_mysql
DB_PASSWORD=sua_senha_mysql
DB_NAME=XE
DB_PORT=3306

# Chave secreta para JWT (token de autenticação)
# Use o comando `openssl rand -hex 32` para gerar uma chave segura
SECRET_KEY=sua_chave_secreta_super_segura

# Credenciais para o usuário Administrador Master
# Estas credenciais serão usadas pelo script de inicialização para criar o primeiro usuário
ADMIN_EMAIL=admin@dominio.com
ADMIN_PASSWORD=senha_forte_para_admin
```

O script de inicialização do banco de dados (`app/database/tables.py`) usa as variáveis `ADMIN_EMAIL` e `ADMIN_PASSWORD` para criar o usuário `admin_master` na primeira execução. Os logs confirmam que a ausência dessas variáveis causa um erro.

---

## 🏃 Executando a Aplicação

Após concluir a instalação, você pode iniciar a aplicação com o Uvicorn.

### 1. Inicializar o Banco de Dados

Execute o script `tables.py` para criar o banco de dados e as tabelas necessárias. Este passo só é necessário na primeira vez.

```bash
python app/database/tables.py
```

Você verá logs indicando a criação de tabelas como `ibdn_usuarios`, `empresa`, e `selo`.

### 2. Iniciar o Servidor FastAPI

Execute o seguinte comando na raiz do projeto:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

* `main:app`: Refere-se ao arquivo `main.py` e à instância `app` do FastAPI.
* `--reload`: Reinicia o servidor automaticamente sempre que um arquivo é alterado.
* `--host 0.0.0.0`: Torna a aplicação acessível na sua rede local.
* `--port 8000`: Define a porta em que a aplicação será executada.

Após a execução, a API estará disponível em **`http://127.0.0.1:8000`** e a documentação interativa (Swagger UI) em **`http://127.0.0.1:8000/docs`**.

---

## 3. Arquitetura do Front-end (Cliente)

A interface do usuário foi desenvolvida como uma Single-Page Application (SPA) utilizando a biblioteca React. Esta abordagem foi escolhida para proporcionar uma experiência de usuário rica, rápida e responsiva.

- **Consumidor da API:** O front-end atua exclusivamente como um consumidor da API RESTful provida pelo backend em FastAPI. Toda a comunicação e manipulação de dados ocorre por meio de requisições HTTP aos endpoints documentados.
- **Responsabilidade e Lógica:** A responsabilidade primária do front-end é a apresentação e a experiência do usuário (UI/UX). Ele não contém regras de negócio críticas; sua função é renderizar os dados recebidos da API e capturar as entradas do usuário para enviá-las ao backend.
- **Arquitetura Baseada em Componentes:** A aplicação é estruturada em componentes reutilizáveis, o que facilita a manutenção, a escalabilidade e a consistência visual da interface.
- **Gerenciamento de Estado:** O estado da aplicação (como informações do usuário autenticado e token) é gerenciado utilizando ferramentas do ecossistema React, como a Context API, garantindo um fluxo de dados previsível.

---

## ⚙️ Configurando e Rodando o Front-end

Para executar o ambiente de desenvolvimento do front-end, siga os passos abaixo.

### 1. Navegue até o diretório do front-end:

Supondo que o código do cliente esteja em uma pasta `frontend/`:

```bash
cd frontend/
```

### 2. Instale as dependências do projeto:

```bash
# Usando npm
npm install

# Ou usando yarn
yarn install
```

### 3. Configure as Variáveis de Ambiente:

Crie um arquivo `.env` na raiz do diretório do front-end (`frontend/.env`) para definir a URL da API do backend.

```env
# Exemplo para Vite
VITE_API_URL=http://127.0.0.1:8000

# Exemplo para Create React App
REACT_APP_API_URL=http://127.0.0.1:8000
```

### 4. Execute o Servidor de Desenvolvimento:

Após a instalação das dependências e com o backend já em execução, inicie o servidor do React.

```bash
# Comando padrão para projetos Vite
npm run dev

# Comando padrão para projetos Create React App
npm start
```

A aplicação front-end estará disponível em **`http://localhost:5173`** ou **`http://localhost:3000`**, conforme a configuração do seu projeto. O backend já está configurado para aceitar requisições dessas origens.
