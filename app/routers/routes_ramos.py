
from fastapi import APIRouter, Path
from logging import info
from app.models.model_ramo import RamoBase, RamoCreate, RamoUpdate
from app.controllers.controller_ramo import (
    get_ramos, get_ramo_by_id, create_ramo, delete_ramo, update_ramo
)
from typing import List

router = APIRouter()

# rotas ramos
@router.get("/ramos", response_model=List[RamoBase])
def listar_ramo():
    return get_ramos()

@router.get("/ramos/{ramo_id}", response_model=RamoBase)
def obter_ramo(ramo_id:int = Path(..., gt=0)):
    return get_ramo_by_id(ramo_id)

@router.post("/ramos",response_model=RamoBase)
def criar_ramo(ramo: RamoCreate):
    return create_ramo(ramo)

@router.put("/ramos/{ramo_id}", response_model=RamoBase)
def atualizar_ramo(ramo_id: int, ramo: RamoBase):
    return update_ramo(ramo_id, ramo)

@router.delete("/ramos/{ramo_id}", status_code=204)
def deletar_ramo(ramo_id:int = Path(..., gt=0)):
   return delete_ramo(ramo_id)