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
    # Corrigido de site_empresas para site_empresa para consistência
    site_empresa: Optional[str] = None
    data_cadastro: datetime
    ativo: bool


class EmpresaCreate(BaseModel):
    cnpj: str = Field(..., max_length=18)
    razao_social: str = Field(..., max_length=255)
    nome_fantasia: Optional[str] = Field(None, max_length=255)
    # Admin pode fornecer, senão é pego do token
    usuario_id: Optional[str] = None
    telefone: Optional[str] = Field(None, max_length=20)
    responsavel: Optional[str] = Field(None, max_length=100)
    cargo_responsavel: Optional[str] = Field(None, max_length=100)
    site_empresa: Optional[str] = Field(None, max_length=255)
    ativo: Optional[bool] = True

    @field_validator("cnpj")
    def validar_e_formatar_cnpj(cls, v):
        # Remove todos os caracteres não numéricos
        cnpj_numerico = re.sub(r'\D', '', v)
        if len(cnpj_numerico) != 14:
            raise ValueError("CNPJ deve conter 14 dígitos.")
        # Formato padrão: XX.XXX.XXX/XXXX-XX
        return f"{cnpj_numerico[:2]}.{cnpj_numerico[2:5]}.{cnpj_numerico[5:8]}/{cnpj_numerico[8:12]}-{cnpj_numerico[12:]}"


class EmpresaDeleteRequest(BaseModel):
    empresa_id: Optional[int] = None


class EmpresaUpdate(BaseModel):
    # Todos os campos são opcionais na atualização
    razao_social: Optional[str] = Field(None, max_length=255)
    nome_fantasia: Optional[str] = Field(None, max_length=255)
    telefone: Optional[str] = Field(None, max_length=20)
    responsavel: Optional[str] = Field(None, max_length=100)
    cargo_responsavel: Optional[str] = Field(None, max_length=100)
    site_empresa: Optional[str] = Field(None, max_length=255)
    ativo: Optional[bool] = None

    # O Pydantic v2 usa model_dump(exclude_unset=True) para não enviar campos não preenchidos,
    # então validadores individuais para cada campo não são estritamente necessários se apenas usarmos max_length.
    # No entanto, se quiséssemos lógicas mais complexas, poderíamos adicioná-las aqui.
