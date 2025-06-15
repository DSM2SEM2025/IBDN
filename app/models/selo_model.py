# app/models/selo_model.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# --- Modelos para o Catálogo de Selos (tabela 'selo') ---


class SeloBase(BaseModel):
    """Modelo base com os campos que definem um tipo de selo."""
    nome: str = Field(..., max_length=100)
    descricao: Optional[str] = None
    sigla: str = Field(..., max_length=10)


class SeloCreate(SeloBase):
    """Modelo para criar um novo tipo de selo no catálogo."""
    pass


class SeloUpdate(BaseModel):
    """Modelo para atualizar um tipo de selo existente no catálogo."""
    nome: Optional[str] = Field(None, max_length=100)
    descricao: Optional[str] = None
    sigla: Optional[str] = Field(None, max_length=10)


class SeloInDB(SeloBase):
    """Modelo que representa um tipo de selo completo, como ele existe no banco de dados."""
    id: int

    class Config:
        from_attributes = True


# --- Modelos para a Instância de Selo Concedido (tabela 'empresa_selo') ---

class ConcederSeloRequest(BaseModel):
    """Corpo da requisição para um admin conceder um selo a uma empresa."""
    id_selo: int = Field(...,
                         description="ID do selo (do catálogo) a ser concedido.")
    dias_validade: int = Field(
        365, gt=0, description="Número de dias que o selo será válido.")


class SeloConcedido(BaseModel):
    """Representa uma instância de selo concedida a uma empresa."""
    id: int  # ID da tabela empresa_selo
    id_empresa: int
    id_selo: int
    status: str
    data_emissao: Optional[date]
    data_expiracao: Optional[date]
    codigo_selo: str

    # Adicionando detalhes do catálogo e da empresa para respostas completas
    nome_selo: str
    sigla_selo: str
    razao_social_empresa: str

    class Config:
        from_attributes = True
