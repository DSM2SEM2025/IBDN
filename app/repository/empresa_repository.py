import mysql.connector
from typing import Dict, Any
from app.database.connection import get_db_connection # Sua função de conexão
from app.models.empresas_model import EmpresaCreate

async def criar_nova_empresa(empresa: EmpresaCreate, usuario_id: int) -> int:
    """
    Insere uma nova empresa no banco de dados.
    Esta função só lida com a lógica de banco de dados.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO empresa(
            cnpj, razao_social, nome_fantasia,
            usuario_id, telefone, responsavel,
            cargo_responsavel, site_empresa, ativo
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            empresa.cnpj,
            empresa.razao_social,
            empresa.nome_fantasia,
            usuario_id, # Usamos o ID que o controller validou
            empresa.telefone,
            empresa.responsavel,
            empresa.cargo_responsavel,
            empresa.site_empresa,
            empresa.ativo
        )
        cursor.execute(sql, values)
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        # Relança o erro para ser tratado pelo controller
        raise Exception(f"Erro de banco de dados: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()