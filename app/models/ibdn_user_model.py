# app/schemas/ibdn_user_schemas.py
import uuid
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

# --- Schemas de Permissão da IBDN ---


class IbdnPermissaoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100,
                      description="Nome descritivo da permissão")


class IbdnPermissaoCreate(IbdnPermissaoBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()),
                    description="ID único da permissão (UUID)")


class IbdnPermissaoUpdate(IbdnPermissaoBase):
    # Ao atualizar, o nome é o único campo editável
    pass


class IbdnPermissao(IbdnPermissaoBase):
    id: str

    class Config:
        from_attributes = True

# --- Schemas de Perfil da IBDN ---


class IbdnPerfilBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=50,
                      description="Nome descritivo do perfil")


class IbdnPerfilCreate(IbdnPerfilBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()),
                    description="ID único do perfil (UUID)")
    permissoes_ids: Optional[List[str]] = Field(
        default_factory=list, description="Lista de IDs de permissões a serem associadas a este perfil na criação")


class IbdnPerfilUpdate(BaseModel):
    nome: Optional[str] = Field(
        None, min_length=3, max_length=50, description="Novo nome para o perfil (opcional)")
    permissoes_ids: Optional[List[str]] = Field(
        None, description="Lista de IDs de permissões para definir para este perfil (substitui as existentes se fornecida)")


class IbdnPerfil(IbdnPerfilBase):
    id: str
    permissoes: List[IbdnPermissao] = Field(
        default_factory=list, description="Lista de permissões associadas a este perfil")

    class Config:
        from_attributes = True

# --- Schema para associar/desassociar permissão de perfil ---


class PerfilPermissaoLink(BaseModel):
    permissao_id: str = Field(...,
                              description="ID da permissão a ser vinculada/desvinculada")

# --- Schemas de Usuário da IBDN ---


class IbdnUsuarioBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    email: EmailStr = Field(...,
                            description="Email do usuário (validação automática)")
    ativo: Optional[bool] = Field(True)
    twofactor: Optional[bool] = Field(False)


class IbdnUsuarioCreate(IbdnUsuarioBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    senha: str = Field(..., min_length=6,
                       description="Senha do usuário (será hasheada)")
    perfil_id: Optional[str] = Field(
        None, description="ID do perfil a ser associado")


class IbdnUsuarioUpdate(BaseModel):
    """Schema usado para atualizar um usuário existente. Todos os campos são opcionais."""
    nome: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr] = None
    perfil_id: Optional[str] = Field(
        None, description="Novo ID do perfil para o usuário (pode ser null para desvincular)")
    ativo: Optional[bool] = None
    twofactor: Optional[bool] = None
    senha: Optional[str] = Field(
        None, min_length=6, description="Nova senha para o usuário (se for alterar)")


class IbdnUsuario(IbdnUsuarioBase):
    id: str
    perfil: Optional[IbdnPerfil] = Field(
        None, description="Perfil completo associado ao usuário")

    class Config:
        from_attributes = True
