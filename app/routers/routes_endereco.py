from fastapi import APIRouter, Path, Depends
from typing import List
from app.controllers.controller_endereco import get_empresa_enderecos_by_empresa_id,update_empresa_endereco
from app.models.model_endereco import EmpresaEndereco,EmpresaEnderecoUpdate
from app.controllers.token import require_permission

router = APIRouter(
    prefix="",
    tags=["Endereco"],
    responses={404: {"description": "Não encontrado"}},
)

@router.get("/empresas/{empresa_id}/enderecos", response_model=List[EmpresaEndereco], dependencies=[Depends(require_permission("empresa", "admin"))])
def listar_enderecos_da_empresa(empresa_id: int = Path(..., gt=0)):
    return get_empresa_enderecos_by_empresa_id(empresa_id)

@router.put("/empresas/{empresa_id}/enderecos/{endereco_id}", dependencies=[Depends(require_permission("empresa", "admin"))])
def atualizar_endereco_da_empresa(
    data: EmpresaEnderecoUpdate,
    empresa_id: int = Path(..., gt=0),
    endereco_id: int = Path(..., gt=0)
):
    return update_empresa_endereco(empresa_id, endereco_id, data.dict())
