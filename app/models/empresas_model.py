from pydantic import BaseModel, field_validator
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
    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str] = None
    usuario_id: int
    telefone: Optional[str] = None
    responsavel: Optional[str] = None
    cargo_responsavel: Optional[str] = None
    site_empresa: Optional[str] = None
    ativo: Optional[bool] = True

    @field_validator("cnpj")
    def validar_cnpj(cls,v):
        if len(v) > 18:
            raise ValueError("CNPJ deve ter no máximo 18 caracteres")
        return v
    
    @field_validator("razao_social")
    def validar_raz_social(cls, x):
        if len(x) > 50:
            raise ValueError("A Razão Social deve ter no máximo 50 caracteres")
        return x

class EmpresaDeleteRequest(BaseModel):
    empresa_id: Optional[int] = None
