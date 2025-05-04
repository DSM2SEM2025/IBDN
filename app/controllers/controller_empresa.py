import mysql.connector
from fastapi import HTTPException
from typing import List
from app.models.empresas_model import Empresa, EmpresaCreate
from app.database.config import get_db_config

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