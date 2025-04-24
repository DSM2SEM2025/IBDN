from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from app.models.database_setup import create_database_if_not_exists, create_tables, setup_logging
import logging

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
    lifespan=lifespan
)


@app.get("/")
def root():
    return {"message": "Sistema de Gerenciamento de Empresas API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
