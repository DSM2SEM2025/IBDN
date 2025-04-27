from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from ..controllers.controller_selo import get_selos_por_empresas

router = APIRouter(
    prefix="/empresas/{empresa_id}/selos",
    tags=["Selos"],
    responses={404: {"description": "Não encontrado"}},
)
@router.get("/", summary="Lista selos fornecidos por uma empresa")
async def listar_selos_empresa(
    empresa_id: int, 
    pagina: int = Query(1, gt=0, description="Número da página"),
    limite: int = Query(10, gt=0, le=100, description="Itens por página"),
    status: Optional[str] = Query(None, description="Filtrar por status (ex: 'ativo', 'expirado')"),
    expiracao_proxima: Optional[bool] = Query(
        None, 
        description="Filtrar selos com expiração próxima (30 dias)"
    ) 
):
    
    return await get_selos_por_empresas(
        empresa_id=empresa_id,
        pagina=pagina,
        limite=limite,
        status=status,
        expiracao_proxima=expiracao_proxima
    )