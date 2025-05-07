import mysql.connector
from mysql.connector import Error
from datetime import datetime
from typing import Optional
from fastapi import HTTPException
from ..repository.selos_repository import get_selos_por_empresas as repo_get_selos, select_selo_empresa

async def get_selos_por_empresas(
    empresa_id: int,
    pagina: int = 1,
    limite: int = 10,
    status: Optional[str] = None,
    expiracao_proxima: Optional[bool] = None
):  
    try:
        resultado = await repo_get_selos(
            empresa_id=empresa_id,
            pagina=pagina,
            limite=limite,
            status=status,
            expiracao_proxima=expiracao_proxima
        )
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar selos: {str(e)}"
        )  

def retornar_empresas_com_selos_criados():
    try:
        selos = select_selo_empresa()
        return selos 
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))