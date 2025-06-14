
from fastapi import APIRouter, Path, Depends
from app.controllers.token import require_permission
from logging import info
from app.models.model_ramo import RamoBase, RamoCreate, RamoUpdate
from app.controllers.controller_ramo import (
    controller_update_ramo,controller_create_ramo,controller_delete_ramo,controller_get_ramo_by_id,controller_get_ramos
)
from typing import List

router = APIRouter(
    prefix="",
    tags=["Ramos"],
    responses={404: {"description": "Não encontrado"}},)

# rotas ramos
@router.get("/ramos", response_model=List[RamoBase], dependencies=[Depends(require_permission("admin"))])
def listar_ramo():
    return controller_get_ramos() #preciso colocar o ID na resposta da rota

@router.get("/ramos/{ramo_id}", response_model=RamoBase, dependencies=[Depends(require_permission("empresa"))])
def obter_ramo(ramo_id:int = Path(..., gt=0)):
    return controller_get_ramo_by_id(ramo_id)

@router.post("/ramos",response_model=RamoBase, dependencies=[Depends(require_permission("empresa"))])
def criar_ramo(ramo: RamoCreate):
    return controller_create_ramo(ramo)

@router.put("/ramos/{ramo_id}", response_model=RamoBase, dependencies=[Depends(require_permission("empresa"))])
def atualizar_ramo(ramo_id: int, ramo: RamoBase):
    return controller_update_ramo(ramo_id, ramo)

@router.delete("/ramos/{ramo_id}", status_code=204, dependencies=[Depends(require_permission("empresa"))])
def deletar_ramo(ramo_id:int = Path(..., gt=0)):
   return controller_delete_ramo(ramo_id)