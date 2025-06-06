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