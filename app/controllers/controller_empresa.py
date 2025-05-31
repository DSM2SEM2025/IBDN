import mysql.connector
from fastapi import HTTPException
from typing import List
from app.database.config import get_db_config
from app.models.empresas_model import Empresa, EmpresaCreate
from app.models.empresas_model import (
    Empresa, EmpresaCreate, EmpresaContatoUpdate, EmpresaRedeSocialUpdate
)

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

# EMPRESA_ENDERECO

def get_empresa_enderecos_by_empresa_id(empresa_id: int):
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM endereco WHERE id_empresa = %s", (empresa_id,))
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        if not rows:
            raise HTTPException(status_code=404, detail="Nenhum endereço encontrado para esta empresa")
        return rows
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar endereços: {err}")

def update_empresa_endereco(empresa_id: int, endereco_id: int, data: dict):
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Verifica se o endereço pertence à empresa
        cursor.execute("SELECT id FROM endereco WHERE id = %s AND id_empresa = %s", (endereco_id, empresa_id))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Endereço não encontrado para esta empresa")

        # Atualiza o endereço
        cursor.execute("""
            UPDATE endereco SET 
                logradouro = %s,
                bairro = %s,
                cep = %s,
                cidade = %s,
                uf = %s,
                complemento = %s
            WHERE id = %s AND id_empresa = %s
        """, (
            data.get('logradouro'),
            data.get('bairro'),
            data.get('cep'),
            data.get('cidade'),
            data.get('uf'),
            data.get('complemento'),
            endereco_id,
            empresa_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return {"mensagem": "Endereço atualizado com sucesso"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar endereço: {err}")