from fastapi import APIRouter, Path, Depends
from app.controllers.token import require_permission
from logging import info
from app.models.model_ramo import RamoBase, RamoCreate, RamoUpdate, RamoResponse
from app.controllers.controller_ramo import (
    controller_update_ramo, controller_create_ramo, controller_delete_ramo, controller_get_ramo_by_id, controller_get_ramos
)
from typing import List

router = APIRouter(
    prefix="/ramos",
    tags=["Ramos"],
    responses={404: {"description": "Não encontrado"}},)


@router.get("/", response_model=List[RamoBase], dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))])
def listar_ramos():
    return controller_get_ramos()


@router.get("/{ramo_id}", response_model=RamoBase, dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))])
def obter_ramo(ramo_id: int = Path(..., gt=0)):
    return controller_get_ramo_by_id(ramo_id)


@router.post("/", response_model=RamoResponse, status_code=201, dependencies=[Depends(require_permission("admin", "admin_master"))])
def criar_ramo(ramo: RamoCreate):
    return controller_create_ramo(ramo)


@router.put("/{ramo_id}", response_model=RamoResponse, dependencies=[Depends(require_permission("admin", "admin_master"))])
def atualizar_ramo(ramo_id: int, ramo: RamoUpdate):
    return controller_update_ramo(ramo_id, ramo)


@router.delete("/{ramo_id}", status_code=204, dependencies=[Depends(require_permission("admin", "admin_master"))])
def deletar_ramo(ramo_id: int = Path(..., gt=0)):
    return controller_delete_ramo(ramo_id)