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


class EmpresaUpdate(BaseModel):
    razao_social: Optional[str] = None
    nome_fantasia: Optional[str] = None
    telefone: Optional[str] = None
    responsavel: Optional[str] = None
    cargo_responsavel: Optional[str] = None
    site_empresa: Optional[str] = None
    ativo: Optional[bool] = None 

    @field_validator("razao_social")
    def validar_razao_social(cls, v):
        if v is not None and len(v) > 50:
            raise ValueError("A Razão Social deve ter no máximo 50 caracteres")
        return v

    @field_validator("site_empresa")
    def validar_site_empresa(cls, v):
        if v is not None and len(v) > 255:
            raise ValueError("O site da empresa deve ter no máximo 255 caracteres")
        return v

    @field_validator("telefone")
    def validar_telefone(cls, v):
        if v is not None and len(v) > 20:
            raise ValueError("O telefone deve ter no máximo 20 caracteres")
        return v

    @field_validator("responsavel")
    def validar_responsavel(cls, v):
        if v is not None and len(v) > 100:
            raise ValueError("O nome do responsável deve ter no máximo 100 caracteres")
        return v

    @field_validator("cargo_responsavel")
    def validar_cargo_responsavel(cls, v):
        # Corrigi o limite que você tinha para 100, para ser consistente com a tabela
        if v is not None and len(v) > 100: 
            raise ValueError("O cargo do responsável deve ter no máximo 100 caracteres")
        return v