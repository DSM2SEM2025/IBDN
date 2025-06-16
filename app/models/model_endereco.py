from pydantic import BaseModel
from typing import Optional

class EmpresaEndereco(BaseModel):
    id: int
    id_empresa: int
    logradouro: str
    numero: str
    bairro: str
    cep: str
    cidade: str
    uf: str
    complemento: Optional[str] = None

    class Config:
        from_attributes = True

class EmpresaEnderecoUpdate(BaseModel):
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    bairro: Optional[str] = None
    cep: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    complemento: Optional[str] = None

class EmpresaEnderecoCreate(BaseModel):
    logradouro: str
    numero: str
    bairro: str
    cep: str
    cidade: str
    uf: str
    complemento: Optional[str] = None
    