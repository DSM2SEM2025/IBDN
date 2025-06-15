# app/routers/routes_tipo_selo.py
from fastapi import APIRouter, Depends, status
from typing import List
from app.controllers import tipo_selo_controller as ctrl
from app.models.tipo_selo_model import TipoSeloInDB, TipoSeloCreate, TipoSeloUpdate
from app.controllers.token import require_permission

router = APIRouter(
    prefix="/tipos_selo",
    tags=["Tipos de Selo"],
    # Protege todas as rotas
    dependencies=[Depends(require_permission("admin", "admin_master"))],
    responses={404: {"description": "Não encontrado"}},
)


@router.post("/", response_model=TipoSeloInDB, status_code=status.HTTP_201_CREATED)
def create_tipo_selo(data: TipoSeloCreate):
    return ctrl.create_tipo_selo(data)


@router.get("/", response_model=List[TipoSeloInDB])
def get_all_tipos_selo():
    return ctrl.get_all_tipos_selo()


@router.get("/{id}", response_model=TipoSeloInDB)
def get_tipo_selo_by_id(id: int):
    return ctrl.get_tipo_selo_by_id(id)


@router.put("/{id}", response_model=TipoSeloInDB)
def update_tipo_selo(id: int, data: TipoSeloUpdate):
    return ctrl.update_tipo_selo(id, data)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_tipo_selo(id: int):
    return ctrl.delete_tipo_selo(id)
