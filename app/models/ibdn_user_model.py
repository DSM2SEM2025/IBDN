# app/schemas/ibdn_user_schemas.py
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional

# --- Schemas de Permissão da IBDN ---


class IbdnPermissaoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100,
                      description="Nome descritivo da permissão")


class IbdnPermissaoCreate(IbdnPermissaoBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()),
                    description="ID único da permissão (UUID)")


class IbdnPermissaoUpdate(IbdnPermissaoBase):
    # Ao atualizar, o nome é o único campo editável além do ID (que não se edita)
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
        [], description="Lista de IDs de permissões a serem associadas a este perfil na criação")


class IbdnPerfilUpdate(BaseModel):
    nome: Optional[str] = Field(
        None, min_length=3, max_length=50, description="Novo nome para o perfil (opcional)")
    permissoes_ids: Optional[List[str]] = Field(
        None, description="Lista de IDs de permissões para definir para este perfil (substitui as existentes se fornecida)")


class IbdnPerfil(IbdnPerfilBase):
    id: str
    permissoes: List[IbdnPermissao] = Field(
        [], description="Lista de permissões associadas a este perfil")

    class Config:
        from_attributes = True

# --- Schema para associar/desassociar permissão de perfil ---


class PerfilPermissaoLink(BaseModel):
    permissao_id: str = Field(...,
                              description="ID da permissão a ser vinculada/desvinculada")

# --- Schemas de Usuário da IBDN (Exemplo, você pode expandir) ---


class IbdnUsuarioBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    # Use EmailStr para validação de email
    email: str = Field(..., description="Email do usuário")
    ativo: Optional[bool] = True
    twofactor: Optional[bool] = False


class IbdnUsuarioCreate(IbdnUsuarioBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    senha: str = Field(..., min_length=6)
    perfil_id: Optional[str] = None


class IbdnUsuario(IbdnUsuarioBase):
    id: str
    # Para exibir o perfil completo associado
    perfil: Optional[IbdnPerfil] = None

    class Config:
        from_attributes = True
