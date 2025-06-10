# app/repository/ibdn_permissions_repository.py
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from mysql.connector import Error  # Importar Error especificamente
# Supondo que get_db_connection está em app.database.connection
from app.database.connection import get_db_connection


def repo_create_ibdn_permissao(permissao_data: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "INSERT INTO ibdn_permissoes (id, nome) VALUES (%s, %s)"
        cursor.execute(query, (permissao_data['id'], permissao_data['nome']))
        conn.commit()
        return permissao_data
    except Error as e:
        conn.rollback()
        if e.errno == 1062:
            raise HTTPException(
                status_code=409, detail=f"Permissão com nome '{permissao_data['nome']}' ou ID '{permissao_data['id']}' já existe.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados ao criar permissão: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_get_ibdn_permissao_by_id(permissao_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, nome FROM ibdn_permissoes WHERE id = %s", (permissao_id,))
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_get_all_ibdn_permissoes(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, nome FROM ibdn_permissoes ORDER BY nome LIMIT %s OFFSET %s", (limit, skip))
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_update_ibdn_permissao(permissao_id: str, nome: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id FROM ibdn_permissoes WHERE id = %s", (permissao_id,))
        if not cursor.fetchone():
            return None

        cursor.execute(
            "UPDATE ibdn_permissoes SET nome = %s WHERE id = %s", (nome, permissao_id))
        conn.commit()
        return {"id": permissao_id, "nome": nome}
    except Error as e:
        conn.rollback()
        if e.errno == 1062:
            raise HTTPException(
                status_code=409, detail=f"Já existe uma permissão com o nome '{nome}'.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados ao atualizar permissão: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_delete_ibdn_permissao(permissao_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM ibdn_permissoes WHERE id = %s", (permissao_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        conn.rollback()
        if e.errno == 1451:
            raise HTTPException(
                status_code=409, detail="Não é possível excluir esta permissão pois ela está associada a um ou mais perfis.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados ao excluir permissão: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
