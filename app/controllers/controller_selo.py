import mysql.connector 
from mysql.connector import Error 
from datetime import datetime
from typing  import Optional 
from fastapi import HTTPException
from ..database.config import get_db_config 
from ..repository.selos_repository import select_selo_empresa, delete_selos_expirados, update_renovar_selo, update_solicitar_renovacao, update_expirar_selo_automatico

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
                e.razao_social
            FROM selo s
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
    try:
        selos = select_selo_empresa()
        return {"dados": selos}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
def remover_selos_expirados():
    return delete_selos_expirados()

def controller_renovar_selo(selo_id: int):
    return update_renovar_selo(selo_id)

def controller_solicitar_renovacao(selo_id: int):
    return update_solicitar_renovacao(selo_id)

def controller_expirar_selo_automatico():
    return update_expirar_selo_automatico()