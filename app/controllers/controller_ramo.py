import mysql.connector
from fastapi import HTTPException
from app.database.config import get_db_config
from typing import List
from app.models.model_ramo import RamoBase,RamoCreate, RamoUpdate, RamoResponse
from app.repository.ramos_repository import get_ramos, get_ramo_by_id,create_ramo, update_ramo

def controller_get_ramos():
    try:
        ramos = get_ramos()
        return ramos
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Erro ao acessar banco: {e}")
    
def controller_get_ramo_by_id(ramo_id:int):
    try:
        row = get_ramo_by_id(ramo_id)
        return row
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Erro ao acessar banco: {e}")
    
def controller_create_ramo(ramo: RamoCreate):
    try:
        criar_ramo = create_ramo(ramo)
        return criar_ramo
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Ramo existente: {e}")
    
    
def controller_update_ramo(ramo_id: int, ramo:RamoBase) -> RamoResponse:
    try:
        atualiza_ramo = update_ramo(ramo_id, ramo)
        return atualiza_ramo
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Erro ao atualizar ramo: {e}")

def controller_delete_ramo(ramo_id:int) -> None:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM ramo WHERE id = %s", (ramo_id,))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Ramo não encontrado")
        
        cursor.execute("DELETE FROM ramo WHERE id = %s", (ramo_id,))
        conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:
        raise HTTPException(status_code=403, detail=(f"{e}"))
    