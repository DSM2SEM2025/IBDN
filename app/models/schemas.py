from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class Empresa(BaseModel):
    id: int
    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str] = None
    usuario_id: int
    telefone: Optional[str] = None
    responsavel: Optional[str] = None
    cargo_responsavel: Optional[str] = None
    site_empresas: Optional[str] = None
    data_cadastro: datetime
    ativo: bool

class EmpresaCreate(BaseModel):
    cnpj: constr(max_length=18)
    razao_social: constr(max_length=50)
    nome_fantasia: Optional[str] = None
    usuario_id: int
    telefone: Optional[str] = None
    responsavel: Optional[str] = None
    cargo_responsavel: Optional[str] = None
    site_empresa: Optional[str] = None
    ativo: Optional[bool] = True