from fastapi import APIRouter
from controllers.controller_empresa import (
    get_empresa_ramos,
    get_empresa_ramos_by_id,
    criar_empresa_ramo,
    update_empresa_ramo,
    delete_empresa_ramo
)
from models.empresa_ramo_model import EmpresaRamoUpdate

router = APIRouter()

@router.get("/empresa-ramo")
def listar_empresa_ramo():
    return get_empresa_ramos

@router.get("/empresa-ramo/{id}")
def lista_empresa_ramo_id(id):
    return get_empresa_ramos_by_id(id)

@router.post("/empresa-ramo", status_code=201)
def post_empresa_ramo(data: EmpresaRamoUpdate):
    return criar_empresa_ramo(data)

@router.post("/empresa-ramo/{id}")
def put_empresa_ramo(id: int, data: EmpresaRamoUpdate):
    return update_empresa_ramo

@router.delete("/empresa-ramo/{id}")
def delete_empresa_ramo_route(id:int):
    return delete_empresa_ramo(id)