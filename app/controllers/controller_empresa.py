import mysql.connector
from fastapi import HTTPException, status
from typing import List, Optional
from app.database.config import get_db_config
from app.models.empresas_model import (
    Empresa, EmpresaCreate, EmpresaDeleteRequest, EmpresaUpdate
)
from app.controllers.token import TokenPayLoad


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
        raise HTTPException(status_code=500, detail=f"Erro ao acessar banco {err}")
    
def criar_empresas(empresa: EmpresaCreate):
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        sql = """
            INSERT INTO empresa(
            cnpj, razao_social, nome_fantasia,
            usuario_id, telefone, responsavel,
            cargo_responsavel, site_empresa, ativo
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            empresa.cnpj,
            empresa.razao_social,
            empresa.nome_fantasia,
            empresa.usuario_id,
            empresa.telefone,
            empresa.responsavel,
            empresa.cargo_responsavel,
            empresa.site_empresa,
            empresa.ativo
        )

        cursor.execute(sql,values)
        conn.commit()

        empresa_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return {"id": empresa_id, "mensagem": "Empresa criada com sucesso"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao criar empresa: {err}")  
        
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
            raise HTTPException(status_code=404, detail="Empresa não encontrada")

        return Empresa(**row)

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar banco: {err}")

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
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Administrador deve fornecer 'empresa_id' no corpo da requisição.")
            empresa_id_to_delete = delete_payload.empresa_id
        elif current_user.tipo_usuario == "Cliente":
            if not current_user.empresa_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário cliente não está associado a uma empresa.")
            empresa_id_to_delete = current_user.empresa_id
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tipo de usuário inválido.")

        # Lógica de Banco de Dados
        cursor.execute("SELECT ativo FROM empresa WHERE id = %s", (empresa_id_to_delete,))
        empresa = cursor.fetchone()

        if not empresa:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Empresa com ID {empresa_id_to_delete} não encontrada.")
        if not empresa['ativo']:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Empresa com ID {empresa_id_to_delete} já se encontra inativa.")

        cursor.execute("UPDATE empresa SET ativo = FALSE WHERE id = %s", (empresa_id_to_delete,))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Falha ao inativar empresa.")

        return {"mensagem": "Empresa excluída com sucesso."}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {err}")
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
            raise HTTPException(status_code=404, detail=f"Empresa com ID {id_empresa} não encontrada.")
        
        empresa_existente = Empresa(**empresa_existente_row)

        # Lógica de Permissão
        if empresa_data.ativo is not None and current_user.tipo_usuario != "ADM":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão negada: apenas administradores podem alterar o status da empresa.")

        if current_user.tipo_usuario == "Cliente":
            if not current_user.empresa_id or current_user.empresa_id != id_empresa:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão negada: você só pode atualizar os dados da sua própria empresa.")
            if not empresa_existente.ativo:
                 raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sua empresa está inativa e não pode ser modificada. Contate um administrador.")

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
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
