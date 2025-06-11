from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificacaoBase(BaseModel):
    mensagem: str
    tipo: str
    lida: bool = False

class NotificacaoCreate(NotificacaoBase):
    pass

class Notificacao(NotificacaoBase):
    id: int
    id_empresa: int
    data_envio: datetime

    class Config:
        from_attributes = True

class NotificacaoUpdate(BaseModel):
    mensagem: Optional[str] = None
    tipo: Optional[str] = None
    lida: Optional[bool] = None