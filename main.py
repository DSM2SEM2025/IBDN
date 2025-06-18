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
    routes_selo,             
    routes_selo_catalogo 
)
from app.service.cors import add_cors
from app.database.tables import create_database_if_not_exists, create_tables, create_initial_data
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()


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

app = FastAPI(
    title="API IBDN",
    version="1.0.0",
    description="API para o sistema de gestão de selos e empresas do IBDN."
)

add_cors(app)

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
app.include_router(routes_selo_catalogo.router) 
app.include_router(routes_selo.router)
print("Routers incluídos com sucesso.")


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API do IBDN!"}


if __name__ == "__main__":
    print("Iniciando servidor de desenvolvimento Uvicorn em http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
