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
    
    # Para empresa_ramo
class EmpresaRamo(BaseModel):
    id: int
    id_empresa: int
    id_ramo: int

class EmpresaRamoUpdate(BaseModel):
    id_empresa: int
    id_ramo: int

# Para empresa_contato
class EmpresaContato(BaseModel):
    id: int
    id_empresa: int
    telefone_comercial: Optional[str] = None
    celular: Optional[str] = None
    whatsapp: Optional[str] = None

class EmpresaContatoUpdate(BaseModel):
    telefone_comercial: Optional[str] = None
    celular: Optional[str] = None
    whatsapp: Optional[str] = None

# Para empresa_rede_social
class EmpresaRedeSocial(BaseModel):
    id: int
    id_empresa: int
    id_tipo_rede_social: int
    url: str

class EmpresaRedeSocialUpdate(BaseModel):
    id_tipo_rede_social: Optional[int] = None
    url: Optional[str] = None
