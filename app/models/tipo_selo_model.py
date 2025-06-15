# app/models/tipo_selo_model.py
from pydantic import BaseModel, Field
from typing import Optional


class TipoSeloBase(BaseModel):
    nome: str = Field(..., max_length=100)
    descricao: str
    sigla: str = Field(..., max_length=10)


class TipoSeloCreate(TipoSeloBase):
    pass


class TipoSeloUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=100)
    descricao: Optional[str] = None
    sigla: Optional[str] = Field(None, max_length=10)


class TipoSeloInDB(TipoSeloBase):
    id: int

    class Config:
        from_attributes = True
