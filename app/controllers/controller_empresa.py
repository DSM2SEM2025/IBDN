import mysql.connector
from fastapi import HTTPException, status
from typing import List, Optional
from app.database.config import get_db_config
from app.models.empresas_model import (
    Empresa, EmpresaCreate, EmpresaDeleteRequest
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

def delete_empresa_by_user(
    delete_payload: Optional[EmpresaDeleteRequest],
    current_user: TokenPayLoad
):
    config = get_db_config()
    conn = None
    cursor = None
    empresa_id_to_delete: Optional[int] = None

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        if current_user.tipo_usuario == "ADM":
            if not delete_payload or delete_payload.empresa_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Administrador deve fornecer 'empresa_id' no corpo da requisição para exclusão."
                )
            empresa_id_to_delete = delete_payload.empresa_id
        elif current_user.tipo_usuario == "Cliente":
            if not current_user.empresa_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Usuário cliente não está associado a uma empresa."
                )
            empresa_id_to_delete = current_user.empresa_id
            # Se o cliente fornecer empresa_id no payload, ele deve corresponder ao seu próprio ou estar ausente
            if delete_payload and delete_payload.empresa_id is not None and delete_payload.empresa_id != current_user.empresa_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Cliente só pode excluir a própria empresa."
                )
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tipo de usuário inválido ou não autorizado.")

        # Verifica se a empresa existe
        cursor.execute("SELECT id, ativo FROM empresa WHERE id = %s", (empresa_id_to_delete,))
        empresa = cursor.fetchone()

        if not empresa:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada.")

        if not empresa['ativo']:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa já se encontra inativa.")

        # Realiza a exclusão lógica: SET ativo = FALSE
        cursor.execute("UPDATE empresa SET ativo = FALSE WHERE id = %s", (empresa_id_to_delete,))
        conn.commit()

        if cursor.rowcount == 0:
            # Este caso idealmente seria capturado pela verificação anterior, mas como uma salvaguarda
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Falha ao atualizar empresa para inativa. Empresa não encontrada ou já inativa.")

        return {"mensagem": "Empresa excluída com sucesso."}

    except mysql.connector.Error as err:
        # Logar erro para depuração
        # print(f"Erro de banco de dados: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro de banco de dados: {err}")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        # Logar erro para depuração
        # print(f"Erro interno do servidor: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno do servidor: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()