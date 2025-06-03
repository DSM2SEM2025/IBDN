from fastapi import APIRouter
from typing import List
from app.controllers.controller_contato import get_empresa_contatos, update_empresa_contato
from app.models.contato_model import EmpresaContato,EmpresaContatoUpdate

router = APIRouter(
    prefix="",
    tags=["Contato"],
    responses={404: {"description": "Não encontrado"}},
)

@router.get("/empresa_contatos", response_model=List[EmpresaContato])
def listar_empresa_contatos():
    return get_empresa_contatos()

@router.put("/empresa_contatos/{id}")
def atualizar_empresa_contato(id: int, data: EmpresaContatoUpdate):
    return update_empresa_contato(id, data)
