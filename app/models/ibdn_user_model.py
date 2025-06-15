# app/models/ibdn_user_model.py
import uuid
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

# --- Schemas de Permissão da IBDN ---


class IbdnPermissaoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100,
                      description="Nome descritivo da permissão (ex: 'admin', 'editar_empresa')")


class IbdnPermissaoCreate(IbdnPermissaoBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()),
                    description="ID único da permissão (UUID)")


class IbdnPermissaoUpdate(BaseModel):
    # Ao atualizar, apenas o nome é editável.
    nome: str = Field(..., min_length=3, max_length=100)


class IbdnPermissao(IbdnPermissaoBase):
    id: str

    class Config:
        from_attributes = True


# --- Schemas de Perfil da IBDN ---

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
    # Se a lista for enviada, ela substituirá completamente as permissões existentes.
    # Enviar uma lista vazia [] removerá todas as permissões.
    permissoes_ids: Optional[List[str]] = Field(
        None,
        description="Lista COMPLETA de IDs de permissões para o perfil (substitui as existentes)")


class IbdnPerfil(IbdnPerfilBase):
    id: str
    permissoes: List[IbdnPermissao] = Field(
        default_factory=list, description="Lista de permissões associadas a este perfil")

    class Config:
        from_attributes = True

# --- Schema para associar/desassociar permissão de perfil (usado em rotas específicas) ---


class PerfilPermissaoLink(BaseModel):
    permissao_id: str = Field(...,
                              description="ID da permissão a ser vinculada/desvinculada")

# --- Schemas de Usuário da IBDN ---


class IbdnUsuarioBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    ativo: bool = True
    twofactor: bool = False


class IbdnUsuarioCreate(IbdnUsuarioBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    senha: str = Field(..., min_length=8,
                       description="Senha do usuário (deve ter no mínimo 8 caracteres)")
    # O perfil_id é opcional na criação. Se não for fornecido, o repositório atribuirá um padrão.
    perfil_id: Optional[str] = Field(
        None, description="ID do perfil a ser associado")


class IbdnUsuarioUpdate(BaseModel):
    """Schema usado para atualizar um usuário existente. Todos os campos são opcionais."""
    nome: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr] = None
    # Pode ser null para desvincular o perfil
    perfil_id: Optional[str] = None
    ativo: Optional[bool] = None
    twofactor: Optional[bool] = None
    # Senha opcional, mas se fornecida, deve ter no mínimo 8 caracteres
    senha: Optional[str] = Field(
        None, min_length=8, description="Nova senha para o usuário (se for alterar)")


class IbdnUsuario(IbdnUsuarioBase):
    id: str
    # O perfil pode ser nulo se o usuário não tiver um perfil associado.
    perfil: Optional[IbdnPerfil] = None

    class Config:
        from_attributes = True
