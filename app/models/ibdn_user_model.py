import uuid
from pydantic import BaseModel, Field, EmailStr,field_validator, model_validator
from typing import List, Optional


class IbdnPermissaoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100,
                      description="Nome descritivo da permissão (ex: 'admin', 'editar_empresa')")


class IbdnPermissaoCreate(IbdnPermissaoBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()),
                      description="ID único da permissão (UUID)")


class IbdnPermissaoUpdate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)


class IbdnPermissao(IbdnPermissaoBase):
    id: str

    class Config:
        from_attributes = True


class IbdnPerfilBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=50,
                      description="Nome descritivo do perfil (ex: 'Administrador', 'Empresa')")


class IbdnPerfilCreate(IbdnPerfilBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()),
                      description="ID único do perfil (UUID)")
    permissoes_ids: Optional[List[str]] = Field(
        default_factory=list,
        description="Lista de IDs de permissões a serem associadas a este perfil na criação")


class IbdnPerfilUpdate(BaseModel):
    nome: Optional[str] = Field(
        None, min_length=3, max_length=50, description="Novo nome para o perfil (opcional)")
    permissoes_ids: Optional[List[str]] = Field(
        None,
        description="Lista COMPLETA de IDs de permissões para o perfil (substitui as existentes)")


class IbdnPerfil(IbdnPerfilBase):
    id: str
    permissoes: List[IbdnPermissao] = Field(
        default_factory=list, description="Lista de permissões associadas a este perfil")

    class Config:
        from_attributes = True


class PerfilPermissaoLink(BaseModel):
    permissao_id: str = Field(...,
                                description="ID da permissão a ser vinculada/desvinculada")


class IbdnUsuarioBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    ativo: bool = True
    twofactor: bool = False


class IbdnUsuarioCreate(IbdnUsuarioBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    senha: str = Field(..., min_length=8,
                       description="Senha do usuário (deve ter no mínimo 8 caracteres)")
    perfil_id: Optional[str] = Field(
        None, description="ID do perfil a ser associado")


class IbdnUsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr] = None
    perfil_id: Optional[str] = None
    ativo: Optional[bool] = None
    twofactor: Optional[bool] = None
    senha: Optional[str] = Field(
        None, min_length=8, description="Nova senha para o usuário (se for alterar)")


class IbdnUsuario(IbdnUsuarioBase):
    id: str
    perfil: Optional[IbdnPerfil] = None

    class Config:
        from_attributes = True

class UsuarioRegister(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    senha: str = Field(..., min_length=8, description="A senha deve ter no mínimo 8 caracteres.")
    senha_confirmacao: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UsuarioRegister':
        pw1 = self.senha
        pw2 = self.senha_confirmacao
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('As senhas não coincidem.')
        return self