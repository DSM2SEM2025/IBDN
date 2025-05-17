import mysql.connector
from mysql.connector import Error
from fastapi import HTTPException

from app.config.config import get_db_config


def get_db_connection():
    try:
        config = get_db_config()
        connection = mysql.connector.connect(**config)
        return connection
    except Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao conectar ao banco de dados: {str(e)}"
        )
