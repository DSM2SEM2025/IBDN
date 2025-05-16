from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
from typing import Optional

class Ramo(Base):
    __tablename__ = 'ramo'
    id = Column(Integer, primary_key=True, index=True)
    id_empresa = Column(Integer, ForeignKey('empresa.id', ondelete="CASCADE"))
    id_tipo_rede_social = Column(Integer, ForeignKey('tipo_rede_social.id', ondelete="SET NULL"), nullable=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)

    empresa = relationship("Empresa")
    tipo_rede_social = relationship("TipoRedeSocial")

class RamoBase(BaseModel):
    id_empresa: int
    id_tipo_rede_social: Optional[int]
    nome: str
    descricao: Optional[str]

class RamoCreate(RamoBase):
    pass

class RamoUpdate(BaseModel):
    nome: Optional[str]
    descricao: Optional[str]
    id_tipo_rede_social: Optional[int]

class RamoOut(RamoBase):
    id: int

    class Config:
        orm_mode = True

