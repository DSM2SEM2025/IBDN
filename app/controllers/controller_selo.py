import mysql.connector 
from mysql.connector import Error 
from datetime import datetime
from typing  import Optional 
from fastapi import HTTPException
from ..database.config import get_db_config 

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
    
async def get_selos_por_empresas(
        empresa_id: int,
        pagina: int = 1,
        limite: int = 10,
        status: Optional[str] = None,
        expiracao_proxima: Optional[bool] = None 
):
        
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            # Query base
            query = """
            SELECT 
                s.id,
                s.codigo_selo,
                s.data_emissao,
                s.data_expiracao,
                s.status,
                DATEDIFF(s.data_expiracao, CURDATE()) AS dias_para_expirar,
                e.nome_fantasia
            FROM selos s
            JOIN empresa e on s.id_empresa = e.id
            WHERE s.id_empresa = %s
            """

            params = [empresa_id]

            if status:
                query += " AND s.status = %s"
                params.append(status)

            if expiracao_proxima is not None:
                if expiracao_proxima:
                      query += " AND s.data_expiracao BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)"
                else:
                      query += "AND (s.data_expiracao < CURDATE() OR s.data_expiracao > DATE_ADD(CURDATE(), INTERVAAL 30 DAY))"
 

            count_query = "SELECT COUNT(*) AS  total FROM (" + query + ") AS subquery"
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

def retornar_empresas_com_selos_criados():
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
        