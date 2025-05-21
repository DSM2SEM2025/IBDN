from pydantic import BaseModel

class EmpresaRamo(BaseModel):
    id: int
    id_empresa: int
    id_ramo: int

class EmpresaRamoUpdate(BaseModel):
    id_empresa: int
    id_ramo: int