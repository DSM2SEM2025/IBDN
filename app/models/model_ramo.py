from pydantic import BaseModel, Field
from typing import Optional

class RamoBase(BaseModel):
    id: Optional[int] = None
    nome: str = Field(..., exemple="Tecnologia")
    descricao: Optional[str] = Field(None, example="Empresas de desenvolvimento")

class RamoCreate(RamoBase):
    pass

class RamoUpdate(RamoBase):
    pass

class RamoResponse(RamoBase):
    id: int

    class Config:
        orm_mode = True