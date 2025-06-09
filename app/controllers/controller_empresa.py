import mysql.connector
from fastapi import HTTPException, status
from typing import List, Optional
from app.database.config import get_db_config
from app.models.empresas_model import (
    Empresa, EmpresaCreate, EmpresaDeleteRequest, EmpresaUpdate
)
from app.controllers.token import TokenPayLoad


def get_empresas() -> List[Empresa]:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * from empresa")
        rows = cursor.fetchall()

        empresas = [Empresa(**row) for row in rows]

        cursor.close()
        conn.close()
        return empresas	
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar banco {err}")
    
def criar_empresas(empresa: EmpresaCreate):
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
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
            empresa.usuario_id,
            empresa.telefone,
            empresa.responsavel,
            empresa.cargo_responsavel,
            empresa.site_empresa,
            empresa.ativo
        )

        cursor.execute(sql,values)
        conn.commit()

        empresa_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return {"id": empresa_id, "mensagem": "Empresa criada com sucesso"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao criar empresa: {err}")  
        
def get_empresa_por_id(empresa_id: int) -> Empresa:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM empresa WHERE id = %s", (empresa_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Empresa não encontrada")

        return Empresa(**row)

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar banco: {err}")

def delete_logically(empresa_id: int) -> bool:
    """
    Executa a exclusão lógica (ativo=False) de uma empresa.
    Retorna True se a exclusão foi bem-sucedida, False caso contrário.
    """
    config = get_db_config()
    conn = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Verifica se a empresa existe e está ativa antes de tentar deletar
        cursor.execute("SELECT ativo FROM empresa WHERE id = %s", (empresa_id,))
        result = cursor.fetchone()
        if not result or not result[0]:
            return False

        # Executa o update para inativar a empresa
        cursor.execute("UPDATE empresa SET ativo = FALSE WHERE id = %s", (empresa_id,))
        conn.commit()
        
        # Retorna True se uma linha foi afetada
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def update_empresa_db(id_empresa: int, empresa_data: EmpresaUpdate) -> Optional[Empresa]:
    """Executa a query UPDATE no banco e retorna os dados atualizados da empresa."""
    config = get_db_config()
    conn = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM empresa WHERE id = %s", (id_empresa,))
        if not cursor.fetchone():
            return None

        update_fields = empresa_data.model_dump(exclude_unset=True)
        if not update_fields:
            return get_empresa_por_id(id_empresa)

        # Constrói a query dinamicamente para atualizar apenas os campos recebidos.
        set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
        sql = f"UPDATE empresa SET {set_clause} WHERE id = %s"
        values = list(update_fields.values()) + [id_empresa]

        cursor.execute(sql, tuple(values))
        conn.commit()
        
        return get_empresa_por_id(id_empresa)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
