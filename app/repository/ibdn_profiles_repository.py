# app/repository/ibdn_profiles_repository.py
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from mysql.connector import Error
# Supondo que get_db_connection está em app.database.connection
from app.database.connection import get_db_connection


def repo_create_ibdn_perfil(perfil_data: Dict[str, Any], permissoes_ids: List[str]) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "INSERT INTO ibdn_perfis (id, nome) VALUES (%s, %s)"
        cursor.execute(query, (perfil_data['id'], perfil_data['nome']))

        if permissoes_ids:
            assoc_query = "INSERT INTO ibdn_perfil_permissoes (perfil_id, permissao_id) VALUES (%s, %s)"
            for p_id in permissoes_ids:
                cursor.execute(assoc_query, (perfil_data['id'], p_id))
        conn.commit()
        return perfil_data
    except Error as e:
        conn.rollback()
        if e.errno == 1062:
            raise HTTPException(
                status_code=409, detail=f"Perfil com nome '{perfil_data['nome']}' ou ID '{perfil_data['id']}' já existe.")
        if e.errno == 1452:
            raise HTTPException(
                status_code=400, detail="Uma ou mais permissões_ids fornecidas não existem.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados ao criar perfil: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_get_ibdn_perfil_by_id_with_permissions(perfil_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    perfil = None
    try:
        cursor.execute(
            "SELECT id, nome FROM ibdn_perfis WHERE id = %s", (perfil_id,))
        perfil = cursor.fetchone()
        if not perfil:
            return None

        perm_query = """
            SELECT p.id, p.nome 
            FROM ibdn_permissoes p
            JOIN ibdn_perfil_permissoes ipp ON p.id = ipp.permissao_id
            WHERE ipp.perfil_id = %s
            ORDER BY p.nome
        """
        cursor.execute(perm_query, (perfil_id,))
        permissoes = cursor.fetchall()
        perfil['permissoes'] = permissoes
        return perfil
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_get_all_ibdn_perfis_with_permissions(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    perfis_completos = []
    try:
        # Primeiro pega os perfis base com paginação
        cursor.execute(
            "SELECT id, nome FROM ibdn_perfis ORDER BY nome LIMIT %s OFFSET %s", (limit, skip))
        perfis_base = cursor.fetchall()

        # Depois, para cada perfil, busca suas permissões
        # Isso é N+1, considere otimizar com JOINs mais complexos ou menos chamadas se performance for crítica
        for perfil_base_data in perfis_base:
            perfil_completo = repo_get_ibdn_perfil_by_id_with_permissions(
                perfil_base_data['id'])
            if perfil_completo:
                perfis_completos.append(perfil_completo)
        return perfis_completos
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_update_ibdn_perfil(perfil_id: str, nome: Optional[str], permissoes_ids: Optional[List[str]]) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Verifica se o perfil existe
        cursor.execute(
            "SELECT id FROM ibdn_perfis WHERE id = %s", (perfil_id,))
        if not cursor.fetchone():
            return None

        if nome is not None:
            cursor.execute(
                "UPDATE ibdn_perfis SET nome = %s WHERE id = %s", (nome, perfil_id))

        if permissoes_ids is not None:
            cursor.execute(
                "DELETE FROM ibdn_perfil_permissoes WHERE perfil_id = %s", (perfil_id,))
            if permissoes_ids:
                assoc_query = "INSERT INTO ibdn_perfil_permissoes (perfil_id, permissao_id) VALUES (%s, %s)"
                for p_id in permissoes_ids:
                    cursor.execute(assoc_query, (perfil_id, p_id))
        conn.commit()
        return repo_get_ibdn_perfil_by_id_with_permissions(perfil_id)
    except Error as e:
        conn.rollback()
        if e.errno == 1062:
            raise HTTPException(
                status_code=409, detail=f"Nome de perfil '{nome}' já em uso.")
        if e.errno == 1452:
            raise HTTPException(
                status_code=400, detail="Uma ou mais permissões_ids fornecidas para atualização não existem.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados ao atualizar perfil: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_delete_ibdn_perfil(perfil_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM ibdn_perfis WHERE id = %s", (perfil_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        conn.rollback()
        if e.errno == 1451:
            raise HTTPException(
                status_code=409, detail="Não é possível excluir este perfil pois ele está referenciado por usuários. Remova ou altere o perfil dos usuários primeiro.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados ao excluir perfil: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_add_permissao_to_perfil(perfil_id: str, permissao_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO ibdn_perfil_permissoes (perfil_id, permissao_id) VALUES (%s, %s)"
        cursor.execute(query, (perfil_id, permissao_id))
        conn.commit()
        return True
    except Error as e:
        conn.rollback()
        if e.errno == 1062:
            raise HTTPException(
                status_code=409, detail="Esta permissão já está associada a este perfil.")
        if e.errno == 1452:
            raise HTTPException(
                status_code=404, detail="Perfil ou Permissão especificados não foram encontrados.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados ao associar permissão ao perfil: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_remove_permissao_from_perfil(perfil_id: str, permissao_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "DELETE FROM ibdn_perfil_permissoes WHERE perfil_id = %s AND permissao_id = %s"
        cursor.execute(query, (perfil_id, permissao_id))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        conn.rollback()
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados ao desassociar permissão do perfil: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
