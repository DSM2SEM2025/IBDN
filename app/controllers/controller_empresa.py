import mysql.connector
from fastapi import HTTPException
from typing import List
from app.models.empresas_model import Empresa, EmpresaCreate
from app.database.config import get_db_config
from app.models.empresas_model import (
    Empresa, EmpresaCreate, EmpresaContatoUpdate, EmpresaRedeSocialUpdate
)
from app.models.empresa_ramo_model import EmpresaRamoUpdate

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
    
    # EMPRESA_RAMO

def criar_empresa_ramo(data: EmpresaRamoUpdate):
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id FROM empresa_ramo
        WHERE id_empresa = %s AND id_ramo = %s
        """, (data.id_empresa, data.id_ramo))
        existente = cursor.fetchone()
        if existente:
            raise HTTPException(status_code=400, detail="Empresa_ramo já existente com esse IDs.")
        
        cursor.execute("""
        INSERT INTO empresa_ramo (id_empresa, id_ramo)
        VALUES (%s, %s)
        """)
        conn.commit()

        novo_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return {"id": novo_id, "mensagem":"Empresa_ramo criada com sucesso"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao criar empresa_ramo {err}")

def get_empresa_ramos():
    config = get_db_config()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM empresa_ramo")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados

def get_empresa_ramos_by_id():
    config = get_db_config()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM empresa_ramo WHERE id = %s", (id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Empresa_ramo não encontrada para exclusão")
    return row

def update_empresa_ramo(id: int, data: EmpresaRamoUpdate):
    config = get_db_config()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Empresa_ramo não encontrada")
    cursor.execute("""
        UPDATE empresa_ramo SET id_empresa = %s, id_ramo = %s WHERE id = %s
    """, (data.id_empresa, data.id_ramo, id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensagem": "Empresa_ramo atualizada com sucesso"}

def delete_empresa_ramo(id: int):
    config = get_db_config()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empresa_ramo WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensagem": "Empresa_ramo deletada com sucesso"}
    
# EMPRESA_CONTATO
def get_empresa_contatos():
    config = get_db_config()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contato")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados

def update_empresa_contato(id: int, data: EmpresaContatoUpdate):
    config = get_db_config()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE contato SET telefone_comercial = %s, celular = %s, whatsapp = %s WHERE id = %s
    """, (data.telefone_comercial, data.celular, data.whatsapp, id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensagem": "Contato atualizado com sucesso"}

# EMPRESA_REDE_SOCIAL
def get_empresa_redes_sociais():
    config = get_db_config()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM rede_social")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return dados

def update_empresa_rede_social(id: int, data: EmpresaRedeSocialUpdate):
    config = get_db_config()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE rede_social SET id_tipo_rede_social = %s, url = %s WHERE id = %s
    """, (data.id_tipo_rede_social, data.url, id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensagem": "Rede social atualizada com sucesso"}

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

def get_empresa_by_id(empresa_id: int) -> Empresa:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM empresa WHERE id = %s", (empresa_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row is None:
            raise HTTPException(status_code=404, detail="Empresa não encontrada")

        return Empresa(**row)

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar empresa: {err}")
