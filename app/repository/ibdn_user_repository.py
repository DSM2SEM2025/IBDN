# app/repository/ibdn_users_repository.py
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from mysql.connector import Error
from app.database.connection import get_db_connection
# Schemas Pydantic
from app.models.ibdn_user_model import IbdnUsuarioCreate, IbdnUsuarioUpdate
from app.security.password import get_password_hash  # Para hashear senhas
# Para buscar detalhes do perfil, precisaremos chamar o repositório de perfis
from app.repository.ibdn_profiles_repository import repo_get_ibdn_perfil_by_id_with_permissions


def _map_user_db_to_schema(user_db_data: Dict[str, Any], perfil_completo: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Mapeia dados do usuário do banco para o formato do schema, incluindo perfil completo."""
    if user_db_data is None:
        return None

    # Converte TINYINT(1) para bool para os campos ativo e twofactor
    user_data_mapped = {
        "id": user_db_data.get("id"),
        "nome": user_db_data.get("nome"),
        "email": user_db_data.get("email"),
        "ativo": bool(user_db_data.get("ativo", 0)),  # Garante que seja bool
        # Garante que seja bool
        "twofactor": bool(user_db_data.get("twofactor", 0)),
        "perfil_id": user_db_data.get("perfil_id"),  # Mantém o perfil_id
        "perfil": perfil_completo  # Adiciona o objeto perfil completo se fornecido
    }
    # Adicionar senha_hash apenas se for para uso interno (ex: autenticação)
    if "senha_hash" in user_db_data:
        user_data_mapped["senha_hash"] = user_db_data["senha_hash"]

    return user_data_mapped


def repo_create_ibdn_usuario(usuario_data: IbdnUsuarioCreate) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    hashed_password = get_password_hash(usuario_data.senha)
    try:
        query = """
            INSERT INTO ibdn_usuarios (id, nome, email, senha_hash, perfil_id, ativo, twofactor)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            usuario_data.id,
            usuario_data.nome,
            usuario_data.email,
            hashed_password,
            usuario_data.perfil_id,
            1 if usuario_data.ativo else 0,
            1 if usuario_data.twofactor else 0
        ))
        conn.commit()
        # Retorna os dados do usuário criado (sem a senha) e com o perfil se houver
        return repo_get_ibdn_usuario_by_id(usuario_data.id)
    except Error as e:
        conn.rollback()
        if e.errno == 1062:
            raise HTTPException(
                status_code=409, detail=f"Usuário com email '{usuario_data.email}' ou ID '{usuario_data.id}' já existe.")
        if e.errno == 1452 and 'perfil_id' in e.msg:  # FK para perfil_id
            raise HTTPException(
                status_code=400, detail=f"Perfil com ID '{usuario_data.perfil_id}' não encontrado.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados ao criar usuário: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_get_ibdn_usuario_by_id(usuario_id: str, include_password_hash: bool = False) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user_db_data = None
    try:
        select_fields = "id, nome, email, perfil_id, ativo, twofactor"
        if include_password_hash:
            select_fields += ", senha_hash"

        query = f"SELECT {select_fields} FROM ibdn_usuarios WHERE id = %s"
        cursor.execute(query, (usuario_id,))
        user_db_data = cursor.fetchone()

        if not user_db_data:
            return None

        perfil_completo = None
        if user_db_data.get("perfil_id"):
            perfil_completo = repo_get_ibdn_perfil_by_id_with_permissions(
                user_db_data["perfil_id"])

        return _map_user_db_to_schema(user_db_data, perfil_completo)
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_get_ibdn_usuario_by_email(email: str, include_password_hash: bool = False) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user_db_data = None
    try:
        select_fields = "id, nome, email, perfil_id, ativo, twofactor"
        if include_password_hash:
            select_fields += ", senha_hash"
        query = f"SELECT {select_fields} FROM ibdn_usuarios WHERE email = %s"
        cursor.execute(query, (email,))
        user_db_data = cursor.fetchone()

        if not user_db_data:
            return None

        perfil_completo = None
        if user_db_data.get("perfil_id"):
            perfil_completo = repo_get_ibdn_perfil_by_id_with_permissions(
                user_db_data["perfil_id"])

        return _map_user_db_to_schema(user_db_data, perfil_completo)
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_get_all_ibdn_usuarios(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    usuarios_finais = []
    try:
        query = "SELECT id, nome, email, perfil_id, ativo, twofactor FROM ibdn_usuarios ORDER BY nome LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, skip))
        usuarios_db = cursor.fetchall()

        for user_db_data in usuarios_db:
            perfil_completo = None
            if user_db_data.get("perfil_id"):
                perfil_completo = repo_get_ibdn_perfil_by_id_with_permissions(
                    user_db_data["perfil_id"])
            usuarios_finais.append(_map_user_db_to_schema(
                user_db_data, perfil_completo))

        return usuarios_finais
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_update_ibdn_usuario(usuario_id: str, usuario_data: IbdnUsuarioUpdate) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Verifica se o usuário existe
    cursor.execute("SELECT id FROM ibdn_usuarios WHERE id = %s", (usuario_id,))
    if not cursor.fetchone():
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
        return None

    fields_to_update = []
    params = []

    if usuario_data.nome is not None:
        fields_to_update.append("nome = %s")
        params.append(usuario_data.nome)
    if usuario_data.email is not None:
        fields_to_update.append("email = %s")
        params.append(usuario_data.email)
    if usuario_data.senha is not None:
        fields_to_update.append("senha_hash = %s")
        params.append(get_password_hash(usuario_data.senha))

    # Permitir desvincular perfil definindo perfil_id como None explicitamente
    if hasattr(usuario_data, 'perfil_id'):  # Verifica se o campo foi enviado
        fields_to_update.append("perfil_id = %s")
        params.append(usuario_data.perfil_id)  # Pode ser None

    if usuario_data.ativo is not None:
        fields_to_update.append("ativo = %s")
        params.append(1 if usuario_data.ativo else 0)
    if usuario_data.twofactor is not None:
        fields_to_update.append("twofactor = %s")
        params.append(1 if usuario_data.twofactor else 0)

    if not fields_to_update:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
        return repo_get_ibdn_usuario_by_id(usuario_id)

    query = f"UPDATE ibdn_usuarios SET {', '.join(fields_to_update)} WHERE id = %s"
    params.append(usuario_id)

    try:
        cursor.execute(query, tuple(params))
        conn.commit()
        return repo_get_ibdn_usuario_by_id(usuario_id)
    except Error as e:
        conn.rollback()
        if e.errno == 1062:
            raise HTTPException(
                status_code=409, detail=f"Email '{usuario_data.email}' já está em uso por outro usuário.")
        if e.errno == 1452 and 'perfil_id' in e.msg:
            raise HTTPException(
                status_code=400, detail=f"Perfil com ID '{usuario_data.perfil_id}' não encontrado para atualização.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados ao atualizar usuário: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def repo_delete_ibdn_usuario(usuario_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # ON DELETE SET NULL na FK de ibdn_usuarios para log_acesso, etc., deve ser considerado
        # ou tratar essas dependências antes de excluir o usuário.
        cursor.execute(
            "DELETE FROM ibdn_usuarios WHERE id = %s", (usuario_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        conn.rollback()
        if e.errno == 1451:  # FK constraint fails
            raise HTTPException(
                status_code=409, detail="Não é possível excluir este usuário pois ele está referenciado em outras tabelas (ex: empresa, logs). Remova ou desvincule essas referências primeiro.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados ao excluir usuário: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
