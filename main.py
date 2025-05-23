import logging
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.tables import create_database_if_not_exists, create_tables, setup_logging
from app.routers import  (
    routes_selo,
    routes_empresa
    )

# Configure logging
logger = setup_logging()
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    try:
        create_database_if_not_exists()
        create_tables()
        logger.info("Database initialized successfully")
        yield
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        # Encerra a aplicação se o banco não puder ser inicializado
        raise SystemExit(f"Database initialization failed: {e}")


app = FastAPI(
    title="Sistema de Gerenciamento de Empresas",
    description="API para gerenciamento de empresas e selos fornecidos",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(routes_selo.router)
app.include_router(routes_empresa.router)

@app.get("/")
def root():
    return {"message": "Sistema de Gerenciamento de Empresas e Selos API",
            "enpoints": {
                "empresas": "/empresas",
                "selos": "/empresas/{empresa_id}/selos"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "initialized"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000,
        log_config=None 
    )
