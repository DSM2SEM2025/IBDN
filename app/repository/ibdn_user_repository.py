# app/repository/ibdn_user_repository.py
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from mysql.connector import Error
from app.database.connection import get_db_connection
# Schemas Pydantic
from app.models.ibdn_user_model import IbdnUsuarioCreate, IbdnUsuarioUpdate
from app.security.password import get_password_hash  # Para hashear senhas
# Para buscar detalhes do perfil, precisaremos chamar o repositório de perfis
from app.repository.ibdn_profiles_repository import repo_get_ibdn_perfil_by_id_with_permissions


def _get_profile_id_by_name(name: str, cursor) -> Optional[str]:
    """Função auxiliar para buscar o ID de um perfil pelo nome."""
    cursor.execute("SELECT id FROM ibdn_perfis WHERE nome = %s", (name,))
    result = cursor.fetchone()
    return result['id'] if result else None


def _map_user_db_to_schema(user_db_data: Dict[str, Any], perfil_completo: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Mapeia dados do usuário do banco para o formato do schema, incluindo perfil completo."""
    if user_db_data is None:
        return None

    # Converte TINYINT(1) para bool para os campos ativo e twofactor
    user_data_mapped = {
        "id": user_db_data.get("id"),
        "nome": user_db_data.get("nome"),
        "email": user_db_data.get("email"),
        "ativo": bool(user_db_data.get("ativo", 0)),
        "twofactor": bool(user_db_data.get("twofactor", 0)),
        "perfil_id": user_db_data.get("perfil_id"),
        "perfil": perfil_completo
    }
    if "senha_hash" in user_db_data:
        user_data_mapped["senha_hash"] = user_db_data["senha_hash"]

    return user_data_mapped


def repo_create_ibdn_usuario(usuario_data: IbdnUsuarioCreate) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    hashed_password = get_password_hash(usuario_data.senha)
    try:
        # Se nenhum perfil_id for fornecido, busca o ID do perfil 'empresa' para usar como padrão
        perfil_id = usuario_data.perfil_id
        if not perfil_id:
            perfil_id = _get_profile_id_by_name("empresa", cursor)
            if not perfil_id:
                # Se o perfil 'empresa' não existir, lança um erro, pois é uma configuração essencial
                raise HTTPException(
                    status_code=500, detail="Perfil 'empresa' padrão não encontrado no sistema.")

        query = """
            INSERT INTO ibdn_usuarios (id, nome, email, senha_hash, perfil_id, ativo, twofactor)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            usuario_data.id,
            usuario_data.nome,
            usuario_data.email,
            hashed_password,
            perfil_id,  # Usa o perfil_id obtido (seja o fornecido ou o padrão)
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
        if e.errno == 1452 and 'perfil_id' in e.msg:
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
        query = f"SELECT {select_fields}, (SELECT id FROM empresa WHERE usuario_id = u.id) as empresa_id FROM ibdn_usuarios u WHERE u.email = %s"
        cursor.execute(query, (email,))
        user_db_data = cursor.fetchone()

        if not user_db_data:
            return None

        perfil_completo = None
        if user_db_data.get("perfil_id"):
            perfil_completo = repo_get_ibdn_perfil_by_id_with_permissions(
                user_db_data["perfil_id"])

        mapped_user = _map_user_db_to_schema(user_db_data, perfil_completo)
        # Adiciona o empresa_id ao payload final, se existir
        if user_db_data.get("empresa_id"):
            mapped_user["empresa_id"] = user_db_data["empresa_id"]

        return mapped_user

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

    update_dict = usuario_data.model_dump(exclude_unset=True)

    if "nome" in update_dict:
        fields_to_update.append("nome = %s")
        params.append(update_dict["nome"])
    if "email" in update_dict:
        fields_to_update.append("email = %s")
        params.append(update_dict["email"])
    if "senha" in update_dict:
        fields_to_update.append("senha_hash = %s")
        params.append(get_password_hash(update_dict["senha"]))
    if "perfil_id" in update_dict:
        fields_to_update.append("perfil_id = %s")
        params.append(update_dict["perfil_id"])
    if "ativo" in update_dict:
        fields_to_update.append("ativo = %s")
        params.append(1 if update_dict["ativo"] else 0)
    if "twofactor" in update_dict:
        fields_to_update.append("twofactor = %s")
        params.append(1 if update_dict["twofactor"] else 0)

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
        # A FK na tabela `empresa` para `usuario_id` é restritiva.
        # É preciso garantir que o usuário não seja dono de uma empresa antes de excluí-lo.
        cursor.execute(
            "SELECT id FROM empresa WHERE usuario_id = %s", (usuario_id,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=409,
                detail="Não é possível excluir este usuário pois ele está associado a uma empresa. Por favor, reatribua ou delete a empresa primeiro."
            )

        cursor.execute(
            "DELETE FROM ibdn_usuarios WHERE id = %s", (usuario_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        conn.rollback()
        if e.errno == 1451:
            raise HTTPException(
                status_code=409, detail="Não é possível excluir este usuário pois ele está referenciado em outras tabelas (ex: logs). Considere inativar o usuário em vez de excluir.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados ao excluir usuário: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
