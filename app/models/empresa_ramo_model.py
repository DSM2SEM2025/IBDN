from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from database import Base
from pydantic import BaseModel
class EmpresaRamo(Base):
    __tablename__ = 'empresa_ramo'
    id = Column(Integer, primary_key=True, index=True)
    id_empresa = Column(Integer, ForeignKey('empresa.id', ondelete="CASCADE"))
    id_ramo = Column(Integer, ForeignKey('ramo.id', ondelete="CASCADE"))

    __table_args__ = (UniqueConstraint('id_empresa', 'id_ramo', name='uix_empresa_ramo'),)

class EmpresaRamoBase(BaseModel):
    id_empresa: int
    id_ramo: int
class EmpresaRamoOut(BaseModel):
    id: int
    id_empresa: int
    id_ramo: int
    empresa_nome: str
    ramo_nome: str
    ramo_descricao: str

    class Config:
        orm_mode = True
        