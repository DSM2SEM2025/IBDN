import mysql.connector 
from mysql.connector import Error
from fastapi import HTTPException
from typing import List
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
 
def get_ramos() -> List[RamoBase]:
    config = get_db_config()
    connection = mysql.connector.connect(**config)    
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT id, nome, descricao FROM ramo
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        ramos = [RamoBase(**row) for row in rows]
        return ramos
    
    except Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar ramos: {str(e)}"
        )
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def get_ramo_by_id(ramo_id: int) -> RamoBase:
    config = get_db_config()
    connection = mysql.connector.connect(**config) 
    cursor = connection.cursor(dictionary=True) 
    try:
        cursor.execute("SELECT * FROM ramo WHERE id = %s", (ramo_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Ramo não encontrado")
        return RamoBase(**row)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar banco: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close() 

def create_ramo(ramo: RamoCreate) -> RamoBase:
    config = get_db_config()
    connection = mysql.connector.connect(**config) 
    cursor = connection.cursor(dictionary=True) 
    try:
        cursor.execute("SELECT * FROM RAMO WHERE nome = %s AND descricao = %s", (ramo.nome, ramo.descricao))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO ramo (nome, descricao) VALUES (%s,%s)",(ramo.nome,ramo.descricao))
        
        connection.commit()
        ramo_id = cursor.lastrowid

        return RamoBase(id=ramo_id, nome=ramo.nome, descricao=ramo.descricao)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir ramo: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close() 

def update_ramo(ramo_id: int, ramo: RamoBase) -> RamoResponse:
    config = get_db_config()
    connection = mysql.connector.connect(**config) 
    cursor = connection.cursor(dictionary=True) 
    try:
        cursor.execute("UPDATE ramo SET nome = %s, descricao = %s WHERE id = %s", (ramo.nome,ramo.descricao,ramo_id))
        connection.commit()

        return RamoResponse(id=ramo_id, nome=ramo.nome, descricao=ramo.descricao)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar ramo: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close() 

def delete_ramo(ramo_id:int) -> None:
    config = get_db_config()
    connection = mysql.connector.connect(**config) 
    cursor = connection.cursor(dictionary=True) 
    try:
        cursor.execute("SELECT id FROM ramo WHERE id = %s", (ramo_id,))
        if cursor.fetchone() is None:
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail="Ramo não encontrado")
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar ramo; {err}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close() 