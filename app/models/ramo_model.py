from database import Base
from pydantic import BaseModel
from typing import Optional

class RamoBase(BaseModel):
    id_empresa: int
    id_tipo_rede_social: Optional[int] = None
    nome: str
    descricao: Optional[str] = None

class RamoBase(BaseModel):
    id_empresa: int
    id_tipo_rede_social: Optional[int] = None
    nome: str
    descricao: Optional[str] = None

class RamoCreate(RamoBase):
    pass

class RamoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    id_tipo_rede_social: Optional[int] = None

class RamoOut(RamoBase):
    id: int