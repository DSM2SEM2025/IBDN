from fastapi import APIRouter, Depends, status
from typing import List
from app.controllers import controller_selo as ctrl
from app.models.selo_model import SeloInDB, SeloCreate, SeloUpdate
from app.controllers.token import require_permission

router = APIRouter(
    prefix="/selos-catalogo",
    tags=["Catálogo de Selos"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post("/", response_model=SeloInDB, status_code=status.HTTP_201_CREATED, summary="Cria um novo tipo de selo no catálogo", dependencies=[Depends(require_permission( "admin", "admin_master"))])
def criar_selo_no_catalogo(data: SeloCreate):
    return ctrl.criar_tipo_selo(data)


@router.get("/", response_model=List[SeloInDB], summary="Lista todos os tipos de selo do catálogo",  dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))])
def listar_selos_do_catalogo():
    return ctrl.listar_tipos_selo()