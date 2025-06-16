# app/repository/ibdn_profiles_repository.py
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from mysql.connector import Error
from app.database.connection import get_db_connection
import json  # Importa a biblioteca JSON


def repo_create_ibdn_perfil(perfil_data: Dict[str, Any], permissoes_ids: List[str]) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        conn.start_transaction()
        query = "INSERT INTO ibdn_perfis (id, nome) VALUES (%s, %s)"
        cursor.execute(query, (perfil_data['id'], perfil_data['nome']))
        if permissoes_ids:
            assoc_query = "INSERT INTO ibdn_perfil_permissoes (perfil_id, permissao_id) VALUES (%s, %s)"
            dados_associacao = [(perfil_data['id'], p_id)
                                for p_id in permissoes_ids]
            cursor.executemany(assoc_query, dados_associacao)
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
        perfil['permissoes'] = permissoes if permissoes else []
        return perfil
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_get_all_ibdn_perfis_with_permissions(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT
                p.id,
                p.nome,
                JSON_ARRAYAGG(
                    IF(perm.id IS NULL, NULL, JSON_OBJECT('id', perm.id, 'nome', perm.nome))
                ) AS permissoes
            FROM
                ibdn_perfis p
            LEFT JOIN
                ibdn_perfil_permissoes ipp ON p.id = ipp.perfil_id
            LEFT JOIN
                ibdn_permissoes perm ON ipp.permissao_id = perm.id
            GROUP BY
                p.id, p.nome
            ORDER BY
                p.nome
            LIMIT %s OFFSET %s;
        """
        cursor.execute(query, (limit, skip))
        perfis_db = cursor.fetchall()

        # CORREÇÃO: Processa o campo 'permissoes' para cada perfil
        for perfil in perfis_db:
            permissoes_str = perfil.get('permissoes')
            if isinstance(permissoes_str, str):
                # Converte a string JSON para uma lista Python
                permissoes_list = json.loads(permissoes_str)
                # Se o resultado for uma lista contendo apenas [None], converte para uma lista vazia
                if permissoes_list and len(permissoes_list) == 1 and permissoes_list[0] is None:
                    perfil['permissoes'] = []
                else:
                    perfil['permissoes'] = permissoes_list
            elif permissoes_str is None:
                perfil['permissoes'] = []

        return perfis_db
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_update_ibdn_perfil(perfil_id: str, nome: Optional[str], permissoes_ids: Optional[List[str]]) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        conn.start_transaction()
        cursor.execute(
            "SELECT id FROM ibdn_perfis WHERE id = %s FOR UPDATE", (perfil_id,))
        if not cursor.fetchone():
            conn.rollback()
            return None
        if nome is not None:
            cursor.execute(
                "UPDATE ibdn_perfis SET nome = %s WHERE id = %s", (nome, perfil_id))
        if permissoes_ids is not None:
            cursor.execute(
                "DELETE FROM ibdn_perfil_permissoes WHERE perfil_id = %s", (perfil_id,))
            if permissoes_ids:
                assoc_query = "INSERT INTO ibdn_perfil_permissoes (perfil_id, permissao_id) VALUES (%s, %s)"
                dados_associacao = [(perfil_id, p_id)
                                    for p_id in permissoes_ids]
                cursor.executemany(assoc_query, dados_associacao)
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
