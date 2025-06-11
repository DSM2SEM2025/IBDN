import mysql.connector 
from mysql.connector import Error
from fastapi import HTTPException
from ..database.config import get_db_config 
from datetime import datetime
from typing import List, Optional

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

def get_notificacoes_by_empresa(empresa_id: int, lida: Optional[bool] = None) -> List[dict]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM notificacao WHERE id_empresa = %s"
        params = [empresa_id]
        
        if lida is not None:
            query += " AND lida = %s"
            params.append(lida)
            
        query += " ORDER BY data_envio DESC"
        
        cursor.execute(query, params)
        return cursor.fetchall()
    except Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar notificações: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()

def create_notificacao(empresa_id: int, notificacao_data: dict) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO notificacao 
        (id_empresa, mensagem, data_envio, tipo, lida) 
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            empresa_id,
            notificacao_data['mensagem'],
            datetime.now(),
            notificacao_data['tipo'],
            notificacao_data.get('lida', False)
        )
        
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar notificação: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()

def update_notificacao(notificacao_id: int, update_data: dict) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM notificacao WHERE id = %s", (notificacao_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Notificação não encontrada")

        set_clause = []
        params = []
        for field, value in update_data.items():
            if value is not None:
                set_clause.append(f"{field} = %s")
                params.append(value)

        if not set_clause:
            raise HTTPException(
                status_code=400,
                detail="Nenhum campo válido para atualizar foi enviado"
            )

        query = f"UPDATE notificacao SET {', '.join(set_clause)} WHERE id = %s"
        params.append(notificacao_id)

        cursor.execute(query, params)
        conn.commit()
        return True
    except Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar notificação: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()


def delete_notificacao(notificacao_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM notificacao WHERE id = %s", (notificacao_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar notificação: {str(e)}"
        )
    finally:
        cursor.close()
        conn.close()