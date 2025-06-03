import mysql.connector
from fastapi import HTTPException
from app.database.config import get_db_config
from typing import List
from app.models.model_ramo import RamoBase,RamoCreate, RamoUpdate, RamoResponse

def get_ramos() -> List[RamoBase]:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, nome, descricao FROM ramo")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        ramos = [RamoBase(**row) for row in rows]
        return ramos
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar banco: {err}")
    
def get_ramo_by_id(ramo_id:int) -> RamoBase:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM ramo WHERE id = %s", (ramo_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:
            raise HTTPException(status_code=404, detail="Ramo não encontrado")

        return RamoBase(**row)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar banco: {err}")
    
def create_ramo(ramo: RamoCreate) -> RamoBase:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("INSERT INTO ramo (nome, descricao) VALUES (%s,%s)", (ramo.nome,ramo.descricao))
        conn.commit()
        ramo_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return RamoBase(id=ramo_id, nome=ramo.nome, descricao=ramo.descricao)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir ramo: {err}")
    
def update_ramo(ramo_id: int, ramo:RamoBase) -> RamoResponse:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("UPDATE ramo SET nome = %s, descricao = %s WHERE id = %s", (ramo.nome,ramo.descricao,ramo_id))
        conn.commit()

        cursor.close()
        conn.close()

        return RamoResponse(id=ramo_id, nome=ramo.nome, descricao=ramo.descricao)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar ramo: {err}")

def delete_ramo(ramo_id:int) -> None:
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

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=(f"Erro ao deletar ramo; {err}"))
    