from fastapi import APIRouter, Path, Depends
from typing import List
from app.models.model_ramo import RamoBase
from app.controllers.controller_empresaRamo import(
     controller_associar_ramos,controller_remover_associacao, controller_listar_ramos_por_empresas
)
from app.models.empresa_ramo_model import EmpresaRamoCreate,EmpresaRamoResponse
from app.controllers.token import require_permission

router = APIRouter(
    prefix="",
    tags=["Empresa_Ramo"],
    responses={404: {"description": "Não encontrado"}},
)

# rotas empresa_ramo

@router.post("/{id_empresa}/ramos/", response_model=List[EmpresaRamoResponse], status_code=201, dependencies=[Depends(require_permission("empresa", "admin"))])
def atrelar_ramos(id_empresa:int = Path(...,gt=0), dados: EmpresaRamoCreate = None):
    return controller_associar_ramos(id_empresa,dados)

@router.get("/{id_empresa}/ramos/", response_model=List[RamoBase], dependencies=[Depends(require_permission("empresa", "admin"))])
def get_ramos_por_empresa(id_empresa:int =Path(...,gt=0)):
    return controller_listar_ramos_por_empresas(id_empresa)

@router.delete("/{id_empresa}/ramos/{id_ramo}/",status_code=204, dependencies=[Depends(require_permission("empresa", "admin"))])
def delete_associacao(id_empresa: int = Path(..., gt=0),id_ramo:int = Path(...,gt=0)):
    return controller_remover_associacao(id_empresa, id_ramo)
