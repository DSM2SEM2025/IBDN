from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class SeloBase(BaseModel):
    nome: str = Field(..., max_length=100)
    descricao: Optional[str] = None
    sigla: str = Field(..., max_length=10)


class SeloCreate(SeloBase):
    pass


class SeloUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=100)
    descricao: Optional[str] = None
    sigla: Optional[str] = Field(None, max_length=10)


class SeloInDB(SeloBase):
    id: int

    class Config:
        from_attributes = True


class SolicitarSeloRequest(BaseModel):
    id_selo: int = Field(..., description="ID do selo do catálogo que a empresa deseja solicitar.")


class ConcederSeloRequest(BaseModel):
    id_selo: int = Field(...,
                         description="ID do selo (do catálogo) a ser concedido.")
    dias_validade: int = Field(
        365, gt=0, description="Número de dias que o selo será válido.")


class SeloConcedido(BaseModel):
    id: int
    id_empresa: int
    id_selo: int
    status: str
    data_emissao: Optional[date]
    data_expiracao: Optional[date]
    codigo_selo: Optional[str] = None
    nome_selo: str
    sigla_selo: str
    razao_social_empresa: str

    class Config:
        from_attributes = True