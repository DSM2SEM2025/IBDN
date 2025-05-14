from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from database import Base

class EmpresaRamo(Base):
    __tablename__ = 'empresa_ramo'
    id = Column(Integer, primary_key=True, index=True)
    id_empresa = Column(Integer, ForeignKey('empresa.id', ondelete="CASCADE"))
    id_ramo = Column(Integer, ForeignKey('ramo.id', ondelete="CASCADE"))

    __table_args__ = (UniqueConstraint('id_empresa', 'id_ramo', name='uix_empresa_ramo'),)