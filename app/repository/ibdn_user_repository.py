# app/repository/ibdn_user_repository.py
import mysql.connector
from mysql.connector import Error
from typing import List, Optional, Dict, Any
from fastapi import HTTPException  # Importar HTTPException
# Supondo que seus caminhos de configuração e conexão sejam estes:
from app.config.config import get_db_config
from app.database.connection import get_db_connection
# Importe seus schemas Pydantic e utilitário de senha
from app.schemas.ibdn_user_schemas import IbdnUsuarioCreate, IbdnUsuarioUpdate
from app.core.security import get_password_hash

# --- Repositório de Permissões da IBDN ---


def repo_create_ibdn_permissao(permissao_data: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "INSERT INTO ibdn_permissoes (id, nome) VALUES (%s, %s)"
        cursor.execute(query, (permissao_data['id'], permissao_data['nome']))
        conn.commit()
        return permissao_data
    except Error as e:
        conn.rollback()
        if e.errno == 1062:  # Violação de chave única (nome ou id)
            raise HTTPException(
                status_code=409, detail=f"Permissão com nome '{permissao_data['nome']}' ou ID '{permissao_data['id']}' já existe.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()


def repo_get_ibdn_permissao_by_id(permissao_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM ibdn_permissoes WHERE id = %s", (permissao_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def repo_get_all_ibdn_permissoes() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM ibdn_permissoes ORDER BY nome")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# --- Repositório de Perfis da IBDN ---


def repo_create_ibdn_perfil(perfil_data: Dict[str, Any], permissoes_ids: List[str]) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "INSERT INTO ibdn_perfis (id, nome) VALUES (%s, %s)"
        cursor.execute(query, (perfil_data['id'], perfil_data['nome']))

        if permissoes_ids:
            assoc_query = "INSERT INTO ibdn_perfil_permissoes (perfil_id, permissao_id) VALUES (%s, %s)"
            for p_id in permissoes_ids:
                cursor.execute(assoc_query, (perfil_data['id'], p_id))
        conn.commit()
        # Para retornar o perfil criado com permissões, você pode precisar de outra consulta.
        # Por simplicidade, retornando os dados de entrada por enquanto.
        created_perfil = {**perfil_data, "permissoes_ids": permissoes_ids}
        return created_perfil
    except Error as e:
        conn.rollback()
        if e.errno == 1062:  # Violação de chave única (nome ou id do perfil)
            raise HTTPException(
                status_code=409, detail=f"Perfil com nome '{perfil_data['nome']}' ou ID '{perfil_data['id']}' já existe.")
        # Violação de chave estrangeira (permissao_id não existe)
        if e.errno == 1452:
            raise HTTPException(
                status_code=400, detail=f"Uma ou mais permissões_ids fornecidas não existem.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()


def repo_get_ibdn_perfil_by_id(perfil_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM ibdn_perfis WHERE id = %s", (perfil_id,))
        perfil = cursor.fetchone()
        if not perfil:
            return None

        perm_query = """
            SELECT p.id, p.nome 
            FROM ibdn_permissoes p
            JOIN ibdn_perfil_permissoes ipp ON p.id = ipp.permissao_id
            WHERE ipp.perfil_id = %s
        """
        cursor.execute(perm_query, (perfil_id,))
        permissoes = cursor.fetchall()
        perfil['permissoes'] = permissoes
        return perfil
    finally:
        cursor.close()
        conn.close()


def repo_get_all_ibdn_perfis() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, nome FROM ibdn_perfis ORDER BY nome")
        perfis = cursor.fetchall()
        for perfil in perfis:  # N+1 queries, otimizar se houver muitos perfis/permissoes
            perm_query = """
                SELECT p.id, p.nome 
                FROM ibdn_permissoes p
                JOIN ibdn_perfil_permissoes ipp ON p.id = ipp.permissao_id
                WHERE ipp.perfil_id = %s
            """
            cursor.execute(perm_query, (perfil['id'],))
            permissoes_data = cursor.fetchall()
            perfil['permissoes'] = permissoes_data
        return perfis
    finally:
        cursor.close()
        conn.close()


def repo_update_ibdn_perfil(perfil_id: str, perfil_update_data: Dict[str, Any], permissoes_ids: Optional[List[str]]) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if 'nome' in perfil_update_data and perfil_update_data['nome'] is not None:
            cursor.execute("UPDATE ibdn_perfis SET nome = %s WHERE id = %s",
                           (perfil_update_data['nome'], perfil_id))

        if permissoes_ids is not None:
            cursor.execute(
                "DELETE FROM ibdn_perfil_permissoes WHERE perfil_id = %s", (perfil_id,))
            if permissoes_ids:  # Se a lista não for vazia, insere as novas associações
                assoc_query = "INSERT INTO ibdn_perfil_permissoes (perfil_id, permissao_id) VALUES (%s, %s)"
                for p_id in permissoes_ids:
                    cursor.execute(assoc_query, (perfil_id, p_id))

        conn.commit()
        # Retorna o perfil atualizado
        return repo_get_ibdn_perfil_by_id(perfil_id)
    except Error as e:
        conn.rollback()
        if e.errno == 1062:  # Violação de nome único ao atualizar
            raise HTTPException(
                status_code=409, detail=f"Nome de perfil '{perfil_update_data['nome']}' já em uso.")
        if e.errno == 1452:  # Violação de FK ao adicionar permissões
            raise HTTPException(
                status_code=400, detail=f"Uma ou mais permissões_ids fornecidas para atualização não existem.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados ao atualizar perfil: {e}")
    finally:
        cursor.close()
        conn.close()

# --- Repositório de Usuários da IBDN ---


def repo_create_ibdn_usuario(usuario_data: IbdnUsuarioCreate) -> Dict[str, Any]:
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
        created_user_data = usuario_data.model_dump(exclude={"senha"})
        return created_user_data
    except Error as e:
        conn.rollback()
        if e.errno == 1062:
            raise HTTPException(
                status_code=409, detail=f"Usuário com email {usuario_data.email} ou ID {usuario_data.id} já existe.")
        if e.errno == 1452:  # Violação de FK (perfil_id não existe)
            raise HTTPException(
                status_code=400, detail=f"Perfil com ID '{usuario_data.perfil_id}' não encontrado.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados ao criar usuário: {e}")
    finally:
        cursor.close()
        conn.close()


def repo_get_ibdn_usuario_by_id(usuario_id: str, include_password_hash: bool = False) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        select_fields = "id, nome, email, perfil_id, ativo, twofactor"
        if include_password_hash:
            select_fields += ", senha_hash"

        query = f"SELECT {select_fields} FROM ibdn_usuarios WHERE id = %s"
        cursor.execute(query, (usuario_id,))
        user = cursor.fetchone()
        # Opcional: se precisar do objeto perfil completo, buscar aqui e adicionar ao dict 'user'
        # if user and user.get('perfil_id'):
        #     perfil_obj = repo_get_ibdn_perfil_by_id(user['perfil_id'])
        #     user['perfil'] = perfil_obj
        return user
    finally:
        cursor.close()
        conn.close()


def repo_get_ibdn_usuario_by_email(email: str, include_password_hash: bool = False) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        select_fields = "id, nome, email, perfil_id, ativo, twofactor"
        if include_password_hash:
            select_fields += ", senha_hash"
        query = f"SELECT {select_fields} FROM ibdn_usuarios WHERE email = %s"
        cursor.execute(query, (email,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def repo_get_all_ibdn_usuarios(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT id, nome, email, perfil_id, ativo, twofactor FROM ibdn_usuarios ORDER BY nome LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, skip))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def repo_update_ibdn_usuario(usuario_id: str, usuario_data: IbdnUsuarioUpdate) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    fields_to_update = []
    params = []

    # Adiciona campos para atualização se presentes nos dados de entrada
    if usuario_data.nome is not None:
        fields_to_update.append("nome = %s")
        params.append(usuario_data.nome)
    if usuario_data.email is not None:
        fields_to_update.append("email = %s")
        params.append(usuario_data.email)
    if usuario_data.senha is not None:  # Lembre-se que a senha aqui é a senha em texto plano
        fields_to_update.append("senha_hash = %s")
        params.append(get_password_hash(usuario_data.senha))
    if usuario_data.perfil_id is not None:  # Permitir definir perfil_id como NULL
        fields_to_update.append("perfil_id = %s")
        params.append(usuario_data.perfil_id)
    if usuario_data.ativo is not None:
        fields_to_update.append("ativo = %s")
        params.append(1 if usuario_data.ativo else 0)
    if usuario_data.twofactor is not None:
        fields_to_update.append("twofactor = %s")
        params.append(1 if usuario_data.twofactor else 0)

    if not fields_to_update:  # Nenhum campo para atualizar
        # Retorna o usuário atual
        return repo_get_ibdn_usuario_by_id(usuario_id)

    query = f"UPDATE ibdn_usuarios SET {', '.join(fields_to_update)} WHERE id = %s"
    params.append(usuario_id)

    try:
        cursor.execute(query, tuple(params))
        conn.commit()
        if cursor.rowcount == 0:  # Nenhum usuário encontrado com esse ID
            return None
        # Retorna o usuário atualizado
        return repo_get_ibdn_usuario_by_id(usuario_id)
    except Error as e:
        conn.rollback()
        if e.errno == 1062:  # Violação de unicidade (email)
            raise HTTPException(
                status_code=409, detail=f"Email '{usuario_data.email}' já está em uso.")
        if e.errno == 1452:  # Violação de FK (perfil_id não existe)
            raise HTTPException(
                status_code=400, detail=f"Perfil com ID '{usuario_data.perfil_id}' não encontrado para atualização.")
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados ao atualizar usuário: {e}")
    finally:
        cursor.close()
        conn.close()


def repo_delete_ibdn_usuario(usuario_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM ibdn_usuarios WHERE id = %s", (usuario_id,))
        conn.commit()
        return cursor.rowcount > 0  # True se uma linha foi deletada
    except Error as e:
        conn.rollback()
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()
