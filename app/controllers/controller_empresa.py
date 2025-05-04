import mysql.connector
from fastapi import HTTPException
from typing import List
from app.models.schemas import Empresa
from app.database.config import get_db_config

def get_empresas() -> List[Empresa]:
    try:
        cursor = get_db_config.cursor(dictionary=True)
        cursor.execute("SELECT * from empresa")
        rows = cursor.fetchall()

        empresas = [Empresa(**row) for row in rows]

        cursor.close()

        return empresas	
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar banco {err}")