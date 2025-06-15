# app/repository/tipo_selo_repository.py
from typing import List, Optional
from app.database.connection import get_db_connection
from app.models.tipo_selo_model import TipoSeloCreate, TipoSeloUpdate


def repo_create_tipo_selo(data: TipoSeloCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # A coluna 'ativo' já tem o valor padrão TRUE no banco de dados, então não precisamos incluí-la no INSERT.
        query = "INSERT INTO tipo_selo (nome, descricao, sigla) VALUES (%s, %s, %s)"
        cursor.execute(query, (data.nome, data.descricao, data.sigla))
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()


def repo_get_all_tipos_selo() -> List[dict]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # CORREÇÃO: Busca apenas os tipos de selo que estão ativos.
        query = "SELECT id, nome, descricao, sigla, ativo FROM tipo_selo WHERE ativo = TRUE ORDER BY nome"
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def repo_get_tipo_selo_by_id(id: int) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # CORREÇÃO: Busca o tipo de selo apenas se ele estiver ativo.
        query = "SELECT id, nome, descricao, sigla, ativo FROM tipo_selo WHERE id = %s AND ativo = TRUE"
        cursor.execute(query, (id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def repo_update_tipo_selo(id: int, data: TipoSeloUpdate) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return True  # Nada para atualizar

        set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
        query = f"UPDATE tipo_selo SET {set_clause} WHERE id = %s"
        params = list(update_data.values()) + [id]

        cursor.execute(query, tuple(params))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()


def repo_delete_tipo_selo(id: int) -> bool:
    """
    Realiza a exclusão LÓGICA (inativação) do tipo de selo.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # CORREÇÃO: Em vez de DELETE, fazemos um UPDATE no campo 'ativo'.
        query = "UPDATE tipo_selo SET ativo = FALSE WHERE id = %s AND ativo = TRUE"
        cursor.execute(query, (id,))
        conn.commit()
        # Retorna True se uma linha foi afetada (inativação bem-sucedida)
        return cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()
