from pydantic import BaseModel, field_validator, Field
from typing import Optional
from datetime import datetime
import re


class Empresa(BaseModel):
    id: int
    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str] = None
    usuario_id: str
    telefone: Optional[str] = None
    responsavel: Optional[str] = None
    cargo_responsavel: Optional[str] = None
    site_empresa: Optional[str] = None
    data_cadastro: datetime
    ativo: bool


class EmpresaCreate(BaseModel):
    cnpj: str = Field(..., max_length=18)
    razao_social: str = Field(..., max_length=255)
    nome_fantasia: Optional[str] = Field(None, max_length=255)
    # MODIFIED: usuario_id is now an optional field in the request body.
    # An admin can provide it to create a company for another user.
    # If not provided, it will default to the current user's ID.
    telefone: Optional[str] = Field(None, max_length=20)
    responsavel: Optional[str] = Field(None, max_length=100)
    cargo_responsavel: Optional[str] = Field(None, max_length=100)
    site_empresa: Optional[str] = Field(None, max_length=255)
    ativo: Optional[bool] = True

    @field_validator("cnpj")
    def validar_e_formatar_cnpj(cls, v):
        cnpj_numerico = re.sub(r'\D', '', v)
        if len(cnpj_numerico) != 14:
            raise ValueError("CNPJ deve conter 14 dígitos.")
        return f"{cnpj_numerico[:2]}.{cnpj_numerico[2:5]}.{cnpj_numerico[5:8]}/{cnpj_numerico[8:12]}-{cnpj_numerico[12:]}"


class EmpresaDeleteRequest(BaseModel):
    empresa_id: Optional[int] = None


class EmpresaUpdate(BaseModel):
    razao_social: Optional[str] = Field(None, max_length=255)
    nome_fantasia: Optional[str] = Field(None, max_length=255)
    telefone: Optional[str] = Field(None, max_length=20)
    responsavel: Optional[str] = Field(None, max_length=100)
    cargo_responsavel: Optional[str] = Field(None, max_length=100)
    site_empresa: Optional[str] = Field(None, max_length=255)
    ativo: Optional[bool] = None
