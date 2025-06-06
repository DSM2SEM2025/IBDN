from fastapi import HTTPException, status
from typing import Optional

from app.models.empresas_model import Empresa, EmpresaUpdate, EmpresaDeleteRequest
from app.controllers import controller_empresa
from app.controllers.token import TokenPayLoad


def update_empresa_service(id_empresa: int, empresa_update_data: EmpresaUpdate, current_user: TokenPayLoad) -> Empresa:
    """Aplica regras de negócio e permissão para atualizar uma empresa."""
    
    empresa_existente = controller_empresa.get_empresa_por_id(id_empresa)
    
    # Apenas administradores podem alterar o status de uma empresa.
    if empresa_update_data.ativo is not None and current_user.tipo_usuario != "ADM":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão negada: apenas administradores podem alterar o status da empresa."
        )

    # Regras de permissão para clientes.
    if current_user.tipo_usuario == "Cliente":
        if not current_user.empresa_id or current_user.empresa_id != id_empresa:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão negada: você só pode atualizar os dados da sua própria empresa."
            )
        if not empresa_existente.ativo:
             raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sua empresa está inativa e não pode ser modificada. Contate um administrador."
            )

    empresa_atualizada = controller_empresa.update_empresa_db(
        id_empresa=id_empresa,
        empresa_data=empresa_update_data
    )
    
    if not empresa_atualizada:
         raise HTTPException(
            status_code=400,
            detail=f"Falha na atualização da empresa com ID {id_empresa}."
        )

    return empresa_atualizada


def delete_empresa_service(delete_payload: Optional[EmpresaDeleteRequest], current_user: TokenPayLoad) -> dict:
    """Aplica regras de negócio e permissão para excluir uma empresa."""
    
    empresa_id_to_delete: Optional[int] = None
    
    # Lógica de permissão para determinar qual ID de empresa deve ser excluído.
    if current_user.tipo_usuario == "ADM":
        if not delete_payload or delete_payload.empresa_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Administrador deve fornecer 'empresa_id' no corpo da requisição."
            )
        empresa_id_to_delete = delete_payload.empresa_id
    elif current_user.tipo_usuario == "Cliente":
        if not current_user.empresa_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário cliente não está associado a uma empresa."
            )
        empresa_id_to_delete = current_user.empresa_id
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tipo de usuário inválido.")
    
    # Delega a operação de banco de dados para o controller.
    success = controller_empresa.delete_logically(empresa_id_to_delete)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empresa com ID {empresa_id_to_delete} não encontrada ou já está inativa."
        )

    return {"mensagem": "Empresa excluída com sucesso."}