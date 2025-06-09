import mysql.connector 
from mysql.connector import Error
from fastapi import HTTPException
from typing import List
from contextlib import contextmanager
from app.database.config import get_db_config 
from app.models.model_ramo import RamoBase,RamoCreate,RamoResponse,RamoUpdate 

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
    
@contextmanager
def get_cursor():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        yield cursor
        connection.commit()
    except:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
 
def get_ramos() -> List[RamoBase]:
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT id, nome, descricao FROM ramo")
            rows = cursor.fetchall()
            ramos = [RamoBase(**row) for row in rows]
            return ramos
    except Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar ramos: {str(e)}"
        )

def get_ramo_by_id(ramo_id: int) -> RamoBase:
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM ramo WHERE id = %s", (ramo_id,))
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Ramo não encontrado")
            return RamoBase(**row)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar banco: {err}")
    
def create_ramo(ramo: RamoCreate) -> RamoBase:
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM RAMO WHERE nome = %s AND descricao = %s", (ramo.nome, ramo.descricao))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO ramo (nome, descricao) VALUES (%s,%s)",(ramo.nome,ramo.descricao))
            ramo_id = cursor.lastrowid

            return RamoBase(id=ramo_id, nome=ramo.nome, descricao=ramo.descricao)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir ramo: {err}")

def update_ramo(ramo_id: int, ramo: RamoUpdate) -> RamoResponse: 
    try:
        with get_cursor() as cursor:
            cursor.execute("UPDATE ramo SET nome = %s, descricao = %s WHERE id = %s", (ramo.nome,ramo.descricao,ramo_id))
        
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Ramo não encontrado")

            return RamoResponse(id=ramo_id, nome=ramo.nome, descricao=ramo.descricao)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar ramo: {err}")

def delete_ramo(ramo_id:int) -> None:
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT id FROM ramo WHERE id = %s", (ramo_id,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="Ramo não encontrado")
            
            cursor.execute("DELETE FROM RAMO WHERE id =%s", (ramo_id,))
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar ramo; {err}")
    