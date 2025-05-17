from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Literal
from uuid import UUID
import re


class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    perfil: Literal['admin', 'moderador', 'usuario'] = 'usuario'
    is_admin: bool = False

    @field_validator('nome')
    def nome_deve_ser_valido(cls, value):
        # Remove espaços extras
        value = value.strip()

        # Verifica se contém apenas letras, espaços e alguns caracteres especiais
        if not re.match(r'^[a-zA-ZÀ-ÿ\s\'-]+$', value):
            raise ValueError(
                'O nome deve conter apenas letras, espaços, apóstrofos ou hífens')

        # Verifica se tem pelo menos 2 partes (nome e sobrenome)
        if len(value.split()) < 2:
            raise ValueError('Por favor, insira nome e sobrenome')

        return value.title()  # Capitaliza corretamente


class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=8, max_length=100)

    @field_validator('senha')
    def senha_deve_ser_forte(cls, value):
        # Verifica se contém pelo menos um número
        if not re.search(r'\d', value):
            raise ValueError('A senha deve conter pelo menos um número')

        # Verifica se contém pelo menos uma letra maiúscula
        if not re.search(r'[A-Z]', value):
            raise ValueError(
                'A senha deve conter pelo menos uma letra maiúscula')

        # Verifica se contém pelo menos um caractere especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError(
                'A senha deve conter pelo menos um caractere especial')

        # Verifica se não contém sequências comuns
        common_sequences = ['123', 'abc', 'qwerty', 'senha', 'password']
        if any(seq in value.lower() for seq in common_sequences):
            raise ValueError('A senha contém sequências muito comuns')

        return value


class UsuarioResponse(UsuarioBase):
    id: int


class CredenciaisLogin(BaseModel):
    email: EmailStr
    senha: str
