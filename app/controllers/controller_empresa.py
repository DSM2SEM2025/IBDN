import mysql.connector
from fastapi import HTTPException
from typing import List
from app.models.empresas_model import Empresa, EmpresaCreate
from app.database.config import get_db_config
from app.models.empresas_model import (
    Empresa, EmpresaCreate, EmpresaContatoUpdate, EmpresaRedeSocialUpdate
)
from app.models.model_ramo import RamoBase,RamoCreate, RamoUpdate
from app.models.empresa_ramo_model import EmpresaRamoCreate, EmpresaRamoResponse

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
# Ramos

def get_ramos() -> List[RamoBase]:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM ramo")
        rows = cursor.fetchall()

        ramos = [RamoBase(**row) for row in rows]

        cursor.close()
        conn.close()

        return [RamoBase(id=row[0], nome=row[1], descricao=row[2]) for row in ramos]
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar banco: {err}")
    
def get_ramo_by_id(ramo_id:int) -> RamoBase:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM ramo WHERE id = %", (ramo_id))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:
            raise HTTPException(status_code=404, detail="Ramo não encontrado")
        
        return RamoBase(**row)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar banco: {err}")
    
def create_ramo(ramo: RamoCreate) -> RamoBase:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("INSERT INTO ramo (nome, descricao) VALUES (%s,%s)", (ramo.nome,ramo.descricao))
        conn.commit()
        ramo_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return RamoBase(id=ramo_id, nome=ramo.nome, descricao=ramo.descricao)
    except mysql.connector.Erro as err:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir ramo: {err}")
    
def update_ramo(ramo_id: int, ramo:RamoUpdate) -> RamoBase:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("UPDATE ramo SET nome = %s, descricao = %s, WHERE id = %s", (ramo.nome,ramo.descricao,ramo_id))
        conn.commit()

        cursor.close()
        conn.close()

        return RamoBase(id=ramo_id, nome=ramo.nome, descricao=ramo.descricao)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar ramo: {err}")

def delete_ramo(ramo_id:int) -> None:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("DELETE * FROM ramo WHERE id = %s", (ramo_id))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Ramo não encontrado")
        
        cursor.execute("DELETE FROM ramo WHERE id = %s", (ramo_id))
        conn.commit()

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=(f"Erro ao deletar ramo; {err}"))
    
# Empresa_ramo

def associar_ramos(id_empresa:int, dados: EmpresaRamoCreate) -> List[EmpresaRamoResponse]:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        associacoes = []

        for id_ramo in dados.ids_ramo:
            cursor.execute(
                "SELECT * FROM empresa_ramo WHERE id_empresa = %s AND id_ramo = %s", (id_empresa, id_ramo)
            )
            if cursor.fetchone():
                continue
        
            cursor.execute(
                "INSER INTO empresa_ramo (id_empresa, id_ramo) VALUES (%s,%s)",(id_empresa, id_ramo)
            )
            conn.commit()

            associacoes.append(
                EmpresaRamoResponse(
                    id=cursor.lastrowid,
                    id_empresa=id_empresa,
                    id_ramo=id_ramo
                )
            )
        cursor.close()
        conn.close()

        if not associacoes:
            raise HTTPException(status_code=400, detail="Nenhuma associação foi criada. Todas já existiam")
        
        return associacoes
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Falha ao assossiar ramo: {err}")
    
def remover_associacao(id_empresa: int, id_ramo:int) -> None:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM empresa_ramo WHERE id_empresa = %s AND id_ramo %s", (id_empresa, id_ramo)
        )
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Associação não encontrada")
        cursor.execute(
            "DELETE FROM empresa_ramo WHERE id_empresa = %s AND id_ramo = %s", (id_empresa,id_ramo)
        )

        conn.commit()

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao remover associação: {err}")
    
def listar_ramos_por_empresas(id_empresa:int) -> List[RamoBase]:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """SELECT r.id, r.nome, r.descricao FROM ramo r INNER JOIN empresa_ramo er ON r.id = er.id_ramo WHERE er.id_empresa = %s""", (id_empresa)
        )

        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        
        ramos = [RamoBase(**row) for row in rows]

        return ramos
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao listar ramos pelas empresas: {err}")
    
    
        
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