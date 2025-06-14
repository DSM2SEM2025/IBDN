from pydantic import BaseModel
from typing import List

class EmpresaRamoCreate(BaseModel):
    ids_ramo: List[int]

    class Config:
        schema_extra = {
            "example": {
                "ids_ramo": [1, 3, 5]
            }
        }

class EmpresaRamoResponse(BaseModel):
    id:int
    id_empresa:int
    id_ramo:int

    class Config:
        orm_mode = True