import mysql.connector 
from mysql.connector import Error
from fastapi import HTTPException
from ..database.config import get_db_config 
from datetime import datetime, timedelta

# mostro todas as empresas e seus respectivos selos
def select_selo_empresa():
    config = get_db_config()
    connection = mysql.connector.connect(**config)
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""SELECT 
            s.id,
            s.codigo_selo,
            s.data_emissao,
            s.data_expiracao,
            s.status,
            DATEDIFF(s.data_expiracao, CURDATE()) AS dias_para_expirar,
            e.id AS id_empresa,
            e.razao_social
            FROM selo s
            JOIN empresa e ON s.id_empresa = e.id 
            """)
        todos_selos = [
            {
                "id": colunm["id"],
                "codigo_selo":colunm["codigo_selo"],
                "data_emissao": colunm["data_emissao"],  
                "data_expiracao": colunm["data_expiracao"],
                "status": colunm["status"],
                "dias_para_expirar": colunm["dias_para_expirar"],
                "id_empresa": colunm["id_empresa"],
                "razao_social": colunm["razao_social"]
            }
            for colunm in cursor.fetchall()
        ]
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
    return todos_selos
        
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
        raise HTTPException(status_code=500, detail=f"Erro ao remover selos expirados: {str(e)}")

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
    if result["status"] != "pendente":
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
    if result["status"] != "expirado":
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
        print({"error":f"erro realizar a expiração: {e}"})
    finally:
        if cursor:
            cursor.close()