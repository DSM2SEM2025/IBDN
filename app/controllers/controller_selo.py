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
                s.sata_emissao,
                s.data_expiraxao,
                s.status,
                DATEDIFF(a.data_expiracao, CURDATE()) AS dias_para_expirar,
                e.razao_social s
            FROM selo s 
            JOIN EMPRESA E on s.id_empresa = e.id
            WHERE s.id_empresa = %s
            """

            params = [empresa_id]

            if status:
                query += " AND s.status = %s"
                params.append(status)

            if expiracao_proxima is not None:
                if expiracao_proxima:
                      query += " AND s.data_espiracao BETWEEN CURDATE{} AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)"
                else:
                     query += "AND (s.data_expiracao < CURDATE() OR s.data_expiracao > DATE_ADD(CURDATE(), INTERVAAL 30 DAY))"


            count_query = "SELECT COUNT(*) AS  total FROM (" + query + ") AS subquery"
            cursor.execute(count_query, params)
            total = cursor.fetchone()["total"]

            query += "ORDER BY s.data_expiracao ASC LIMIT %s OFFSET %s"
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