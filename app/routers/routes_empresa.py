from fastapi import APIRouter
from typing import List
from app.models.empresas_model import Empresa, EmpresaCreate
from app.controllers.controller_empresa import get_empresas, criar_empresas
from fastapi import Path
from app.controllers.controller_empresa import get_empresas, criar_empresas, get_empresa_por_id
from app.models.empresas_model import (
    EmpresaContato, EmpresaContatoUpdate,
    EmpresaRedeSocial, EmpresaRedeSocialUpdate,
    EmpresaEndereco, EmpresaEnderecoUpdate
)
from app.controllers.controller_empresa import (
    get_empresa_ramos, update_empresa_ramo,
    get_empresa_contatos, update_empresa_contato,
    get_empresa_redes_sociais, update_empresa_rede_social,
    get_empresa_enderecos_by_empresa_id, update_empresa_endereco
)
from app.models.empresa_ramo_model import (
    EmpresaRamo, EmpresaRamoUpdate
)

router = APIRouter()

@router.get("/empresas", response_model=List[Empresa])
def listar_empresas():
    return get_empresas()

@router.post("/empresas")
def adcionar_empresa(empresa: EmpresaCreate):
    return criar_empresas(empresa)

@router.get("/empresa_ramos", response_model=List[EmpresaRamo])
def listar_empresa_ramos():
    return get_empresa_ramos()

@router.put("/empresa_ramos/{id}")
def atualizar_empresa_ramo(id: int, data: EmpresaRamoUpdate):
    return update_empresa_ramo(id, data)

@router.get("/empresa_contatos", response_model=List[EmpresaContato])
def listar_empresa_contatos():
    return get_empresa_contatos()

@router.put("/empresa_contatos/{id}")
def atualizar_empresa_contato(id: int, data: EmpresaContatoUpdate):
    return update_empresa_contato(id, data)

@router.get("/empresa_redes_sociais", response_model=List[EmpresaRedeSocial])
def listar_redes_sociais():
    return get_empresa_redes_sociais()

@router.put("/empresa_redes_sociais/{id}")
def atualizar_rede_social(id: int, data: EmpresaRedeSocialUpdate):
    return update_empresa_rede_social(id, data)

@router.get("/empresas/{empresa_id}", response_model=Empresa)
def buscar_empresa_por_id(empresa_id: int = Path(..., gt=0)):
    return get_empresa_por_id(empresa_id)

@router.get("/empresas/{empresa_id}/enderecos", response_model=List[EmpresaEndereco])
def listar_enderecos_da_empresa(empresa_id: int = Path(..., gt=0)):
    return get_empresa_enderecos_by_empresa_id(empresa_id)

@router.put("/empresas/{empresa_id}/enderecos/{endereco_id}")
def atualizar_endereco_da_empresa(
    empresa_id: int = Path(..., gt=0), 
    endereco_id: int = Path(..., gt=0), 
    data: EmpresaEnderecoUpdate
):
    return update_empresa_endereco(empresa_id, endereco_id, data.dict())