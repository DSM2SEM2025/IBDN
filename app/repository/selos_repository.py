import mysql.connector 
from mysql.connector import Error 
from fastapi import HTTPException
from ..database.config import get_db_config 


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
        