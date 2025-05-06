from typing  import Optional 
from fastapi import HTTPException
from ..repository.selos_repository import get_selos_por_empresas


async def listar_selos_por_empresa(
    empresa_id: int,
    pagina: int = 1,
    limite: int = 10,
    status: Optional[str] = None,
    expiracao_proxima: Optional[bool] = None 
):  


    try:

        resultado = await get_selos_por_empresas(
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