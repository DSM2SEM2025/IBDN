from fastapi import APIRouter, Path
from typing import List
from app.models.empresas_model import (
    Empresa, EmpresaCreate
)
from app.controllers.controller_empresa import (
    get_empresas, criar_empresas, get_empresa_por_id
)

router = APIRouter(
    prefix="",
    tags=["Empresa"],
    responses={404: {"description": "Não encontrado"}},)

@router.get("/empresas", response_model=List[Empresa])
def listar_empresas():
    return get_empresas()

@router.post("/empresas")
def adcionar_empresa(empresa: EmpresaCreate):
    return criar_empresas(empresa)

@router.get("/empresas/{empresa_id}", response_model=Empresa)
def buscar_empresa_por_id(empresa_id: int = Path(..., gt=0)):
    return get_empresa_por_id(empresa_id)
