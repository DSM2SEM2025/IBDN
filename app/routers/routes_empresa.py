from fastapi import APIRouter
from typing import List
from app.models.schemas import Empresa
from app.controllers.controller_empresa import get_empresas

router = APIRouter()

@router.get("/empresas", response_model=List[Empresa])
def listar_empresas():
    return get_empresas()