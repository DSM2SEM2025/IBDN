import mysql.connector
from fastapi import HTTPException, status
from typing import List, Optional, Dict, Any
from app.database.config import get_db_config
from app.models.empresas_model import (
    Empresa, EmpresaCreate, EmpresaDeleteRequest, EmpresaUpdate
)
from app.controllers.token import TokenPayLoad
from app.repository import empresa_repository, ibdn_user_repository

def get_empresas() -> List[Empresa]:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * from empresa")
        rows = cursor.fetchall()

        empresas = [Empresa(**row) for row in rows]

        cursor.close()
        conn.close()
        return empresas
    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Erro ao acessar banco {err}")


async def criar_empresa(empresa_data: EmpresaCreate, current_user: TokenPayLoad) -> Dict[str, Any]:
    """
    Controller para criar uma nova empresa.
    - Se o usuário for admin, ele pode especificar um usuario_id.
    - Se não for admin, a empresa é associada ao seu próprio usuario_id.
    """
    usuario_id_associado = None
    permissoes_do_usuario = set(current_user.permissoes)

    # Verifica se o usuário é admin ou admin_master
    if permissoes_do_usuario.intersection({"admin", "admin_master"}):
        # Se for admin, ele PODE fornecer um usuario_id no payload
        if empresa_data.usuario_id:
            # Verificação extra: O usuário que ele está tentando associar existe?
            usuario_alvo = await ibdn_user_repository.repo_get_ibdn_usuario_by_id(empresa_data.usuario_id)
            if not usuario_alvo:
                raise HTTPException(status_code=404, detail=f"Usuário com ID {empresa_data.usuario_id} não encontrado.")
            usuario_id_associado = empresa_data.usuario_id
        else:
            # Se o admin não especificar, associa a ele mesmo
            usuario_id_associado = current_user.usuario_id
    else:
        # Se NÃO for admin (ex: um usuário 'empresa' ou outro perfil)
        # Verificação de segurança: impede que um usuário já ligado a uma empresa crie outra
        if current_user.empresa_id:
             raise HTTPException(status_code=403, detail="Você já está associado a uma empresa.")
        
        # A empresa será associada OBRIGATORIAMENTE ao seu próprio ID
        usuario_id_associado = current_user.usuario_id

    # O controller não fala com o banco, ele chama o repositório
    # Passamos o 'usuario_id_associado' validado para o repositório
    try:
        nova_empresa_id = await empresa_repository.criar_nova_empresa(empresa_data, usuario_id_associado)
        
        # Opcional: Após criar a empresa, atualize o token do usuário para incluir o novo empresa_id
        # (Isso exigiria uma lógica de atualização de usuário aqui)

        return {"id": nova_empresa_id, "mensagem": "Empresa criada com sucesso"}

    except Exception as e:
        # O repositório pode levantar exceções (ex: CNPJ duplicado)
        raise HTTPException(status_code=500, detail=f"Erro ao criar empresa: {e}")


def get_empresa_por_id(empresa_id: int) -> Empresa:
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM empresa WHERE id = %s", (empresa_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:
            raise HTTPException(
                status_code=404, detail="Empresa não encontrada")

        return Empresa(**row)

    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Erro ao acessar banco: {err}")


def delete_empresa(delete_payload: Optional[EmpresaDeleteRequest], current_user: TokenPayLoad) -> dict:
    """Aplica permissões e realiza a exclusão lógica da empresa."""

    config = get_db_config()
    conn = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        empresa_id_to_delete: Optional[int] = None

        # Lógica de Permissão
        if current_user.tipo_usuario == "ADM":
            if not delete_payload or delete_payload.empresa_id is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Administrador deve fornecer 'empresa_id' no corpo da requisição.")
            empresa_id_to_delete = delete_payload.empresa_id
        elif current_user.tipo_usuario == "Cliente":
            if not current_user.empresa_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Usuário cliente não está associado a uma empresa.")
            empresa_id_to_delete = current_user.empresa_id
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Tipo de usuário inválido.")

        # Lógica de Banco de Dados
        cursor.execute("SELECT ativo FROM empresa WHERE id = %s",
                       (empresa_id_to_delete,))
        empresa = cursor.fetchone()

        if not empresa:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Empresa com ID {empresa_id_to_delete} não encontrada.")
        if not empresa['ativo']:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Empresa com ID {empresa_id_to_delete} já se encontra inativa.")

        cursor.execute(
            "UPDATE empresa SET ativo = FALSE WHERE id = %s", (empresa_id_to_delete,))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Falha ao inativar empresa.")

        return {"mensagem": "Empresa excluída com sucesso."}

    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def update_empresa(id_empresa: int, empresa_data: EmpresaUpdate, current_user: TokenPayLoad) -> Empresa:
    """Aplica permissões, regras de negócio e atualiza a empresa no banco."""

    config = get_db_config()
    conn = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM empresa WHERE id = %s", (id_empresa,))
        empresa_existente_row = cursor.fetchone()
        if not empresa_existente_row:
            raise HTTPException(
                status_code=404, detail=f"Empresa com ID {id_empresa} não encontrada.")

        empresa_existente = Empresa(**empresa_existente_row)

        # Lógica de Permissão
        if empresa_data.ativo is not None and current_user.tipo_usuario != "ADM":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Permissão negada: apenas administradores podem alterar o status da empresa.")

        if current_user.tipo_usuario == "Cliente":
            if not current_user.empresa_id or current_user.empresa_id != id_empresa:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Permissão negada: você só pode atualizar os dados da sua própria empresa.")
            if not empresa_existente.ativo:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Sua empresa está inativa e não pode ser modificada. Contate um administrador.")

        # Lógica de Banco de Dados
        update_fields = empresa_data.model_dump(exclude_unset=True)
        if not update_fields:
            return empresa_existente

        set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
        sql = f"UPDATE empresa SET {set_clause} WHERE id = %s"
        values = list(update_fields.values()) + [id_empresa]

        cursor.execute(sql, tuple(values))
        conn.commit()

        # Busca e retorna o dado atualizado
        cursor.execute("SELECT * FROM empresa WHERE id = %s", (id_empresa,))
        empresa_final = cursor.fetchone()
        return Empresa(**empresa_final)

    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500, detail=f"Erro de banco de dados: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
