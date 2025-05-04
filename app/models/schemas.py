from pydantic import BaseModel
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