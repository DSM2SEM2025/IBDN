# main.py
from app.routers import (
    routes_login,
    routes_empresa,
    routes_ramos,
    routes_empresaRamo,
    routes_endereco,
    routes_notificacao,
    ibdn_users_routes,
    ibdn_profiles_routes,
    ibdn_permissions_routes,
    routes_selo,             # Rota para instâncias de selos
    routes_selo_catalogo     # Rota para o catálogo de selos
)
from app.service.cors import add_cors
from app.database.tables import create_database_if_not_exists, create_tables, create_initial_data
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Importa as funções de configuração e inicialização

# Importa todos os routers da aplicação

# Inicializa o banco de dados e as tabelas antes de iniciar a aplicação
try:
    print("Iniciando a aplicação...")
    print("Verificando e criando banco de dados, se necessário...")
    create_database_if_not_exists()
    print("Verificando e criando tabelas, se necessário...")
    create_tables()
    print("Verificando e populando dados iniciais, se necessário...")
    create_initial_data()
    print("Inicialização do banco de dados concluída com sucesso.")
except Exception as e:
    print(
        f"Ocorreu um erro crítico durante a inicialização do banco de dados: {e}")
    # Considerar encerrar a aplicação se o banco de dados for essencial
    # exit(1)

# Cria a instância principal da aplicação FastAPI
app = FastAPI(
    title="API IBDN",
    version="1.0.0",
    description="API para o sistema de gestão de selos e empresas do IBDN."
)

# Adiciona o middleware de CORS para permitir requisições do frontend
add_cors(app)

# Inclui todos os routers na aplicação
print("Incluindo routers na aplicação...")
app.include_router(routes_login.router)
app.include_router(ibdn_users_routes.router)
app.include_router(ibdn_profiles_routes.router)
app.include_router(ibdn_permissions_routes.router)
app.include_router(routes_empresa.router)
app.include_router(routes_ramos.router)
app.include_router(routes_empresaRamo.router)
app.include_router(routes_endereco.router)
app.include_router(routes_notificacao.router)
app.include_router(routes_selo_catalogo.router)  # Novo router para o catálogo
# Router atualizado para instâncias
app.include_router(routes_selo.router)
print("Routers incluídos com sucesso.")


@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para verificar se a API está online."""
    return {"message": "Bem-vindo à API do IBDN!"}


# Bloco para executar a aplicação em modo de desenvolvimento
if __name__ == "__main__":
    print("Iniciando servidor de desenvolvimento Uvicorn em http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
