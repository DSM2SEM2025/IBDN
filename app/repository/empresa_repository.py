import mysql.connector
from typing import List, Dict, Any, Optional
from app.database.connection import get_db_connection
from app.models.empresas_model import Empresa, EmpresaCreate, EmpresaUpdate


def repo_get_empresa_by_id(empresa_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM empresa WHERE id = %s", (empresa_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def repo_get_all_empresas() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM empresa WHERE ativo = TRUE")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def repo_criar_nova_empresa(empresa: EmpresaCreate, usuario_id: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM empresa WHERE cnpj = %s",
                       (empresa.cnpj,))
        if cursor.fetchone():
            raise mysql.connector.Error(
                errno=1062, msg=f"CNPJ '{empresa.cnpj}' já cadastrado.")

        sql = """
            INSERT INTO empresa(
            cnpj, razao_social, nome_fantasia,
            usuario_id, telefone, responsavel,
            cargo_responsavel, site, ativo
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            empresa.cnpj,
            empresa.razao_social,
            empresa.nome_fantasia,
            usuario_id,
            empresa.telefone,
            empresa.responsavel,
            empresa.cargo_responsavel,
            empresa.site,
            empresa.ativo
        )
        cursor.execute(sql, values)
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        conn.rollback()
        raise Exception(f"Erro de banco de dados: {err.msg}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def repo_update_empresa(empresa_id: int, update_data: EmpresaUpdate) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        update_fields = update_data.model_dump(exclude_unset=True)
        if not update_fields:
            return True

        set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
        sql = f"UPDATE empresa SET {set_clause} WHERE id = %s"
        values = list(update_fields.values()) + [empresa_id]

        cursor.execute(sql, tuple(values))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        conn.rollback()
        raise Exception(f"Erro de banco de dados ao atualizar empresa: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def repo_delete_empresa(empresa_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = "UPDATE empresa SET ativo = FALSE WHERE id = %s AND ativo = TRUE"
        cursor.execute(sql, (empresa_id,))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        conn.rollback()
        raise Exception(f"Erro de banco de dados ao inativar empresa: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()