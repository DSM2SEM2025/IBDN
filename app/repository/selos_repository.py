import mysql.connector
from mysql.connector import Error
from fastapi import HTTPException
from ..database.config import get_db_config
from datetime import datetime, timedelta
from typing import Optional
from ..models.selo_model import AssociacaoMultiplaRequest


def get_db_connection():
    try:
        config = get_db_config()
        connection = mysql.connector.connect(**config)
        return connection
    except Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao conectar ao banco de dados: {str(e)}"
        )

# REMOVA a função antiga 'select_selo_empresa' completamente.

# NOVA FUNÇÃO 1: Para buscar um selo específico.


def get_selo_by_id(selo_id: int):
    """Busca os dados de um único selo pelo seu ID, sem join com empresa."""
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT id, codigo_selo, data_emissao, data_expiracao, status FROM selo WHERE id = %s"
        cursor.execute(query, (selo_id,))
        selo = cursor.fetchone()
        return selo
    except Error as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar selo por ID: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

# NOVA FUNÇÃO 2: Para listar todas as associações.


def get_all_associacoes():
    """Busca todas as associações existentes entre empresas e selos."""
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                s.id, s.codigo_selo, s.status,
                e.id AS id_empresa, e.razao_social
            FROM empresa_selo es
            JOIN selo s ON es.id_selo = s.id
            JOIN empresa e ON es.id_empresa = e.id
            ORDER BY e.razao_social, s.id
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar associações: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


async def get_selos_por_empresas(
        empresa_id: int,
        pagina: int = 1,
        limite: int = 10,
        status: Optional[str] = None,
        expiracao_proxima: Optional[bool] = None
):
    config = get_db_config()
    connection = mysql.connector.connect(**config)
    try:
        cursor = connection.cursor(dictionary=True)
        check_query = "SELECT 1 FROM empresa WHERE id = %s"
        cursor.execute(check_query, (empresa_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail=f"Empresa com ID {empresa_id} não encontrada."
            )
        # Query base
        query = """
                SELECT 
                    s.id,
                    s.codigo_selo,
                    s.data_emissao,
                    s.data_expiracao,
                    s.status,
                    DATEDIFF(s.data_expiracao, CURDATE()) AS dias_para_expirar,
                    e.razao_social
                FROM empresa_selo es
                JOIN selo s ON es.id_selo = s.id
                JOIN empresa e ON es.id_empresa = e.id
                WHERE es.id_empresa = %s
            """
        params = [empresa_id]

        if status:
            query += " AND s.status = %s"
            params.append(status)

        if expiracao_proxima is not None:
            if expiracao_proxima:
                query += " AND s.data_expiracao BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)"
            else:
                query += "AND (s.data_expiracao < CURDATE() OR s.data_expiracao > DATE_ADD(CURDATE(), INTERVAL 30 DAY))"

        count_query = "SELECT COUNT(*) AS  total FROM (" + \
            query + ") AS subquery"
        cursor.execute(count_query, params)
        total = cursor.fetchone()["total"]

        query += " ORDER BY s.data_expiracao ASC LIMIT %s OFFSET %s"
        offset = (pagina - 1) * limite
        params.extend([limite, offset])

        cursor.execute(query, params)
        selos = cursor.fetchall()

        return {
            "empresa_id": empresa_id,
            "pagina": pagina,
            "total": total,
            "selos": selos

        }
    except Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar selos: {str(e)}"
        )
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def delete_selos_expirados():
    config = get_db_config()
    connection = mysql.connector.connect(**config)
    try:
        cursor = connection.cursor(dictionary=True)
        # Deletar os selos com status 'expirado' e expiração superior a 30 dias atrás
        query = """
            DELETE FROM selo
            WHERE status = 'expirado'
              AND data_expiracao < DATE_SUB(CURDATE(), INTERVAL 30 DAY);
        """
        cursor.execute(query)
        connection.commit()

        selos_excluidos = cursor.rowcount

        if selos_excluidos == 0:
            return {"mensagem": "Nenhum selo expirado há mais de 30 dias foi encontrado para remoção."}
        else:
            return {"mensagem": f"{selos_excluidos} selo(s) expirado(s) removido(s) com sucesso."}

    except Error as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao remover selos expirados: {str(e)}")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def update_renovar_selo(selo_id: int):
    config = get_db_config()
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    # Verifica o status atual
    cursor.execute("SELECT status FROM selo WHERE id = %s", (selo_id,))
    result = cursor.fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Selo não encontrado")
    if result["status"].lower() != "pendente":
        raise HTTPException(status_code=400, detail="Selo não está pendente")

    # Atualiza status e datas
    hoje = datetime.now().date()
    nova_expiracao = hoje + timedelta(days=30)

    cursor.execute(
        """
        UPDATE selo 
        SET status = 'ativo', data_emissao = %s, data_expiracao = %s
        WHERE id = %s
        """,
        (hoje, nova_expiracao, selo_id)
    )
    conn.commit()
    return {"message": "Selo aprovado e ativado com sucesso!"}


def update_solicitar_renovacao(selo_id: int):
    config = get_db_config()
    connection = mysql.connector.connect(**config)

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT status FROM selo WHERE id = %s", (selo_id,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Selo não encontrado")
    if result["status"].lower() != "expirado":
        raise HTTPException(status_code=400, detail="Selo não está expirado")

    cursor.execute(
        "UPDATE selo SET status = 'pendente' WHERE id = %s",
        (selo_id,)
    )
    connection.commit()
    return {"message": "Renovação solicitada (pendente de aprovação)"}


def update_expirar_selo_automatico():
    config = get_db_config()
    connection = mysql.connector.connect(**config)
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        hoje = datetime.now().date()

        cursor.execute(
            """
        UPDATE selo 
        SET status = 'expirado'
        WHERE status = 'ativo' AND data_expiracao < %s
        """,
            (hoje,)
        )
        connection.commit()
        print(f"Selos expirados: {cursor.rowcount}")
    except Exception as e:
        print({"error": f"erro realizar a expiração: {e}"})
    finally:
        if cursor:
            cursor.close()


def update_rejeitar_renovacao(selo_id: int, motivo: str = ""):
    """
    Rejeita a renovação de um selo, alterando o status de pendente para expirado.
    """
    config = get_db_config()
    connection = mysql.connector.connect(**config)

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT status FROM selo WHERE id = %s", (selo_id,))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Selo não encontrado")
        if result["status"].lower() != "pendente":
            raise HTTPException(
                status_code=400, detail="Selo não está pendente")

        cursor.execute(
            "UPDATE selo SET status = 'expirado' WHERE id = %s",
            (selo_id,)
        )
        if motivo:
            empresa_query = "SELECT id_empresa FROM selo WHERE id = %s"
            cursor.execute(empresa_query, (selo_id,))
            empresa_result = cursor.fetchone()

            if empresa_result:
                empresa_id = empresa_result["id_empresa"]
                data_envio = datetime.now()
                mensagem = f"Renovação de selo rejeitada. Motivo: {motivo}"

                notificacao_query = """
                INSERT INTO notificacao (id_empresa, mensagem, data_envio, tipo, lida)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(
                    notificacao_query,
                    (empresa_id, mensagem, data_envio, "rejeicao_renovacao", False)
                )

        connection.commit()
        return {"message": "Renovação de selo rejeitada com sucesso"}

    except HTTPException as e:
        raise e
    except Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao rejeitar renovação do selo: {str(e)}"
        )
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def repo_associa_selos_empresa(id_empresa: int, data: AssociacaoMultiplaRequest):
    """
    Cria uma nova instância de selo com código padronizado e a associa
    imediatamente a uma empresa dentro de uma única transação.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM empresa WHERE id = %s", (id_empresa,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404, detail=f"Empresa com ID {id_empresa} não encontrada.")

        cursor.execute(
            "SELECT sigla, nome FROM tipo_selo WHERE id = %s", (data.id_tipo_selo,))
        tipo_selo = cursor.fetchone()
        if not tipo_selo:
            raise HTTPException(
                status_code=400, detail=f"Tipo de selo com ID {data.id_tipo_selo} não existe.")

        query_conflito = "SELECT 1 FROM empresa_selo es JOIN selo s ON es.id_selo = s.id WHERE es.id_empresa = %s AND s.id_tipo_selo = %s"
        cursor.execute(query_conflito, (id_empresa, data.id_tipo_selo))
        if cursor.fetchone():
            raise HTTPException(
                status_code=409, detail=f"Conflito: A empresa já possui um selo do tipo '{tipo_selo['nome']}'.")

        ano_atual = datetime.now().year
        sigla = tipo_selo['sigla']
        codigo_selo_gerado = f"{sigla}-{ano_atual}-{id_empresa}"

        data_emissao = datetime.now().date()
        data_expiracao = data_emissao + timedelta(days=data.dias_validade)
        status = "ativo"

        query_insert_selo = """
            INSERT INTO selo (id_tipo_selo, data_emissao, data_expiracao, codigo_selo, status)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert_selo, (data.id_tipo_selo,
                       data_emissao, data_expiracao, codigo_selo_gerado, status))
        novo_selo_id = cursor.lastrowid

        query_insert_assoc = "INSERT INTO empresa_selo (id_empresa, id_selo) VALUES (%s, %s)"
        cursor.execute(query_insert_assoc, (id_empresa, novo_selo_id))

        connection.commit()

        cursor.execute("SELECT * FROM selo WHERE id = %s", (novo_selo_id,))
        selo_criado = cursor.fetchone()

        return {
            "message": "Selo criado e associado com sucesso!",
            "associacao": {
                "id_empresa": id_empresa,
                "id_selo": novo_selo_id
            },
            "selo_criado": selo_criado
        }

    except HTTPException as http_exc:
        connection.rollback()
        raise http_exc
    except Error as db_err:
        connection.rollback()
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados: {str(db_err)}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
