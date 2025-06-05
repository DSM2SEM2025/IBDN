from pydantic import BaseModel
from typing import Optional

# Para empresa_contato
class EmpresaContato(BaseModel):
    id: int
    id_empresa: int
    telefone_comercial: Optional[str] = None
    celular: Optional[str] = None
    whatsapp: Optional[str] = None

class EmpresaContatoUpdate(BaseModel):
    telefone_comercial: Optional[str] = None
    celular: Optional[str] = None
    whatsapp: Optional[str] = None
