from fastapi import APIRouter
from typing import List
from app.models.schemas import Empresa, EmpresaCreate
from app.controllers.controller_empresa import get_empresas, criar_empresas

router = APIRouter()

@router.get("/empresas", response_model=List[Empresa])
def listar_empresas():
    return get_empresas()

@router.post("/empresas")
def adcionar_empresa(empresa: EmpresaCreate):
    return criar_empresas