import mysql.connector
from mysql.connector import Error
from fastapi import HTTPException
from ..database.connection import get_db_connection
from datetime import datetime, timedelta
from typing import List, Optional

def repo_criar_selo(selo_data: dict) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO selo (nome, descricao, sigla) VALUES (%s, %s, %s)"
        cursor.execute(query, (selo_data['nome'], selo_data.get(
            'descricao'), selo_data['sigla']))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        conn.rollback()
        if e.errno == 1062:
            raise HTTPException(
                status_code=409, detail=f"Já existe um selo com o mesmo nome ou sigla.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()


def repo_listar_selos() -> List[dict]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT id, nome, descricao, sigla FROM selo ORDER BY nome"
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def repo_get_selo_por_id(id_selo: int) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT id, nome, descricao, sigla FROM selo WHERE id = %s"
        cursor.execute(query, (id_selo,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def repo_conceder_selo_empresa(id_empresa: int, id_selo: int, dias_validade: int) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        conn.start_transaction()

        cursor.execute("SELECT 1 FROM empresa WHERE id = %s", (id_empresa,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404, detail="Empresa não encontrada.")

        cursor.execute(
            "SELECT sigla, nome FROM selo WHERE id = %s", (id_selo,))
        selo_catalogo = cursor.fetchone()
        if not selo_catalogo:
            raise HTTPException(
                status_code=404, detail="Tipo de selo não encontrado no catálogo.")

        timestamp = int(datetime.now().timestamp())
        codigo_selo_gerado = f"{selo_catalogo['sigla']}-{datetime.now().year}-{id_empresa}-{timestamp}"
        data_emissao = datetime.now().date()
        data_expiracao = data_emissao + timedelta(days=dias_validade)

        query = """
            INSERT INTO empresa_selo 
            (id_empresa, id_selo, status, data_emissao, data_expiracao, codigo_selo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (id_empresa, id_selo, 'Ativo',
                               data_emissao, data_expiracao, codigo_selo_gerado))
        novo_empresa_selo_id = cursor.lastrowid
        conn.commit()

        return {"id": novo_empresa_selo_id, "codigo_selo": codigo_selo_gerado}

    except Error as e:
        conn.rollback()
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados ao conceder selo: {e}")
    finally:
        cursor.close()
        conn.close()


def repo_listar_selos_da_empresa(id_empresa: int) -> List[dict]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT
                es.id, es.id_empresa, es.id_selo, es.status, es.data_emissao, es.data_expiracao, es.codigo_selo,
                es.plano_solicitado_anos,
                s.nome as nome_selo,
                s.sigla as sigla_selo,
                e.razao_social as razao_social_empresa
            FROM empresa_selo es
            JOIN selo s ON es.id_selo = s.id
            JOIN empresa e ON es.id_empresa = e.id
            WHERE es.id_empresa = %s
            ORDER BY es.data_expiracao DESC
        """
        cursor.execute(query, (id_empresa,))
        return cursor.fetchall()
    except Error as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar selos da empresa: {e}")
    finally:
        cursor.close()
        conn.close()


def repo_listar_solicitacoes_pendentes() -> List[dict]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT
                es.id, es.id_empresa, es.id_selo, es.status, es.data_emissao, es.data_expiracao, es.codigo_selo,
                es.plano_solicitado_anos,
                s.nome as nome_selo,
                s.sigla as sigla_selo,
                e.razao_social as razao_social_empresa
            FROM empresa_selo es
            JOIN selo s ON es.id_selo = s.id
            JOIN empresa e ON es.id_empresa = e.id
            WHERE es.status IN ('Pendente', 'Em Renovação')
            ORDER BY es.data_emissao ASC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar solicitações pendentes: {e}")
    finally:
        cursor.close()
        conn.close()


def repo_atualizar_status_selo(empresa_selo_id: int, novo_status: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if novo_status == 'Ativo':
            cursor.execute("SELECT plano_solicitado_anos FROM empresa_selo WHERE id = %s", (empresa_selo_id,))
            resultado = cursor.fetchone()
            
            anos_validade = 1
            if resultado and resultado.get('plano_solicitado_anos'):
                anos_validade = resultado['plano_solicitado_anos']

            dias_validade = anos_validade * 365
            data_emissao = datetime.now().date()
            data_expiracao = data_emissao + timedelta(days=dias_validade)
            
            query = "UPDATE empresa_selo SET status = %s, data_emissao = %s, data_expiracao = %s WHERE id = %s"
            params = (novo_status, data_emissao, data_expiracao, empresa_selo_id)
        else:
            query = "UPDATE empresa_selo SET status = %s WHERE id = %s"
            params = (novo_status, empresa_selo_id)

        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        conn.rollback()
        raise HTTPException(
            status_code=500, detail=f"Erro ao atualizar status do selo: {e}")
    finally:
        cursor.close()
        conn.close()

def repo_solicitar_selo_empresa(id_empresa: int, id_selo: int, plano_anos: int) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM empresa WHERE id = %s AND ativo = TRUE", (id_empresa,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Empresa não encontrada ou inativa.")

        cursor.execute("SELECT sigla FROM selo WHERE id = %s", (id_selo,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Tipo de selo não encontrado no catálogo.")

        cursor.execute(
            "SELECT id, status FROM empresa_selo WHERE id_empresa = %s AND id_selo = %s",
            (id_empresa, id_selo)
        )
        selo_existente = cursor.fetchone()
        if selo_existente:
            status_existente = selo_existente['status']
            raise HTTPException(
                status_code=409,
                detail=f"Não é possível solicitar este selo. Você já possui uma instância com o status: '{status_existente}'."
            )

        query = "INSERT INTO empresa_selo (id_empresa, id_selo, status, plano_solicitado_anos) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (id_empresa, id_selo, 'Pendente', plano_anos))
        novo_id = cursor.lastrowid
        conn.commit()

        return {"id_solicitacao": novo_id, "mensagem": "Selo solicitado com sucesso. Aguardando aprovação do administrador."}

    except HTTPException:
        raise
    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()

def repo_get_empresa_selo_por_id(empresa_selo_id: int) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT id, id_empresa, id_selo, status, plano_solicitado_anos FROM empresa_selo WHERE id = %s"
        cursor.execute(query, (empresa_selo_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def repo_revogar_selo_empresa(empresa_selo_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "DELETE FROM empresa_selo WHERE id = %s"
        cursor.execute(query, (empresa_selo_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro de banco de dados ao revogar o selo: {e}"
        )
    finally:
        cursor.close()
        conn.close()