import logging
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Importa a função correta de inicialização
from app.database.tables import create_database_if_not_exists, create_tables, setup_logging, create_initial_data
from app.service.cors import add_cors

# Importa os módulos de rotas sem duplicatas
from app.routers import (
    routes_selo,
    routes_empresa,
    routes_empresaRamo,
    routes_ramos,
    routes_endereco,
    routes_notificacao,
    routes_login,
    ibdn_profiles_routes,
    ibdn_permissions_routes,
    ibdn_users_routes
)

# Configura o logging
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    Executa o setup do banco de dados na inicialização.
    """
    logger.info("Iniciando a aplicação...")
    try:
        # Ordem correta de inicialização
        create_database_if_not_exists()
        create_tables()
        # CORREÇÃO: Chama a nova função que cria todos os dados iniciais
        create_initial_data()
        logger.info(
            "Banco de dados e dados iniciais verificados/criados com sucesso.")
        yield
    except Exception as e:
        logger.error(f"Falha ao inicializar o banco de dados: {e}")
        # Encerra a aplicação se o banco não puder ser inicializado
        raise SystemExit(f"Falha na inicialização do banco de dados: {e}")


app = FastAPI(
    title="Sistema de Gerenciamento de Empresas",
    description="API para gerenciamento de empresas e selos fornecidos",
    version="1.0.0",
    lifespan=lifespan
)

# Adiciona as políticas de CORS
add_cors(app)

# Inclui os routers na aplicação
app.include_router(routes_selo.router)
app.include_router(routes_empresa.router)
app.include_router(routes_ramos.router)
app.include_router(routes_empresaRamo.router)
app.include_router(routes_endereco.router)
app.include_router(routes_notificacao.router)
app.include_router(routes_login.router)
app.include_router(ibdn_profiles_routes.router)
app.include_router(ibdn_permissions_routes.router)
app.include_router(ibdn_users_routes.router)


@app.get("/", summary="Endpoint Raiz", tags=["Root"])
def root():
    """Endpoint principal que fornece informações sobre a API."""
    return {
        "message": "API do Sistema de Gerenciamento de Empresas e Selos",
        "enpoints_example": {
            "docs": "/docs",
            "login": "/login",
            "empresas": "/empresas",
            "selos_da_empresa": "/selos/empresa/{empresa_id}",
            "usuarios": "/usuario",
            "perfis": "/perfis",
            "permissoes": "/permissoes",
        }
    }


@app.get("/health", summary="Verificação de Saúde", tags=["Health"])
def health_check():
    """Verifica se a aplicação está operacional."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        log_config=None  # Desativa o logger padrão do uvicorn para usar o nosso
    )
