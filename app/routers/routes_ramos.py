# teste_1/back/app/routers/routes_ramos.py

from fastapi import APIRouter, Path, Depends
from app.controllers.token import require_permission
from logging import info
from app.models.model_ramo import RamoBase, RamoCreate, RamoUpdate, RamoResponse
from app.controllers.controller_ramo import (
    controller_update_ramo, controller_create_ramo, controller_delete_ramo, controller_get_ramo_by_id, controller_get_ramos
)
from typing import List

router = APIRouter(
    prefix="/ramos",  # MODIFICAÇÃO: Removido o prefixo "" para deixar a rota mais limpa
    tags=["Ramos"],
    responses={404: {"description": "Não encontrado"}},)

# Listar todos os ramos - Permissão para admin E empresa, pois a empresa precisa ver para se associar.


@router.get("/", response_model=List[RamoBase], dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))])
def listar_ramos():
    # A resposta já inclui o ID, pois RamoBase foi atualizado para RamoResponse no controller
    return controller_get_ramos()

# Obter um ramo específico por ID - Permissão mantida.


@router.get("/{ramo_id}", response_model=RamoBase, dependencies=[Depends(require_permission("empresa", "admin", "admin_master"))])
def obter_ramo(ramo_id: int = Path(..., gt=0)):
    return controller_get_ramo_by_id(ramo_id)

# MODIFICAÇÃO: Apenas administradores podem criar novos ramos.


@router.post("/", response_model=RamoResponse, status_code=201, dependencies=[Depends(require_permission("admin", "admin_master"))])
def criar_ramo(ramo: RamoCreate):
    return controller_create_ramo(ramo)

# MODIFICAÇÃO: Apenas administradores podem atualizar ramos existentes.


@router.put("/{ramo_id}", response_model=RamoResponse, dependencies=[Depends(require_permission("admin", "admin_master"))])
def atualizar_ramo(ramo_id: int, ramo: RamoUpdate):
    return controller_update_ramo(ramo_id, ramo)

# MODIFICAÇÃO: Apenas administradores podem deletar ramos.


@router.delete("/{ramo_id}", status_code=204, dependencies=[Depends(require_permission("admin", "admin_master"))])
def deletar_ramo(ramo_id: int = Path(..., gt=0)):
    return controller_delete_ramo(ramo_id)
