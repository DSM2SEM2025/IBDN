from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from uuid import UUID


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    perfil: Literal['admin', 'moderador', 'usuario'] = 'usuario'
    is_admin: bool = False


class UsuarioCreate (BaseModel):
    senha: str = Field(..., min_length=6)


class UsuarioResponse(UsuarioBase):
    id: UUID


class CredenciaisLogin(BaseModel):
    email: EmailStr
    senha: str
