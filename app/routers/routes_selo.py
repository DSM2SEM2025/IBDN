from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from ..controllers.controller_selo import get_selos_por_empresas, retornar_empresas_com_selos_criados, remover_selos_expirados, controller_renovar_selo, controller_solicitar_renovacao, controller_expirar_selo_automatico

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

router = APIRouter(
    prefix="/selos",
    tags=["Selos"],
    responses={404: {"description": "Não encontrado"}},
)


@router.get("/empresa/{empresa_id}", summary="Lista selos fornecidos por uma empresa")
async def listar_selos_empresa(
    empresa_id: int,
    pagina: int = Query(1, gt=0, description="Número da página"),
    limite: int = Query(10, gt=0, le=100, description="Itens por página"),
    status: Optional[str] = Query(
        None, description="Filtrar por status (ex: 'ativo', 'expirado')"),
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


@router.get("/todos_selos", summary="Listar todos os selos e quais empresas adquiriram", status_code=200)
async def pegar_todos_selos_empresas_existentes():
    try:
        selos = retornar_empresas_com_selos_criados()
        return {"dados": selos}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/selos_expirados/remover", summary="Remover selos expirados há mais de 30 dias")
async def rota_remover_selos_expirados():
    return remover_selos_expirados()

# PUT para Admin (pendente → ativo)


@router.put("/aprovar/{selo_id}")
def aprovar_selo(selo_id: int):
    return controller_renovar_selo(selo_id)

# Matheus - Criar o rota ou função PUT para Admin(pendente → expirado)
# Caso a IBDN não aprove que o selo da empresa seja renovado - Olhar o exaclidraw , la eu coloquei um bloco sobre isso


# PUT para Cliente (expirado → pendente)
@router.put("/solicitar-renovacao/{selo_id}/")
def solicitar_renovacao(selo_id: int):
    return controller_solicitar_renovacao(selo_id)


# lógica Automática (ativo → expirado)
# Função para o job (chamada externamente)
def expirar_selos_automaticamente():
    return controller_expirar_selo_automatico()


@router.on_event("startup")
def realizar_evento():
    scheduler.add_job(expirar_selos_automaticamente, 'interval', minutes=1)
    scheduler.start()


@router.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()
