from fastapi import HTTPException
from app.repository import endereco_repository as repo
from app.models.model_endereco import EmpresaEnderecoUpdate, EmpresaEnderecoCreate
from app.controllers.token import TokenPayLoad


def get_empresa_enderecos_by_empresa_id(empresa_id: int, current_user: TokenPayLoad):
    is_admin = "admin" in current_user.permissoes or "admin_master" in current_user.permissoes
    if not is_admin and current_user.empresa_id != empresa_id:
        raise HTTPException(status_code=403, detail="Acesso negado.")


def update_empresa_endereco(empresa_id: int, data: EmpresaEnderecoUpdate, current_user: TokenPayLoad):
    # --- INÍCIO DO BLOCO DE SEGURANÇA ---
    is_admin = "admin" in current_user.permissoes or "admin_master" in current_user.permissoes
    
    # Se o usuário NÃO for admin, o ID da empresa na URL DEVE ser igual ao do token
    if not is_admin and current_user.empresa_id != empresa_id:
        raise HTTPException(
            status_code=403, 
            detail="Acesso negado: Você não tem permissão para atualizar o endereço desta empresa."
        )
    # --- FIM DO BLOCO DE SEGURANÇA ---

     # O código só continua se a verificação for aprovada
    updated = repo.update_endereco(empresa_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Nenhum endereço encontrado para esta empresa para ser atualizado.")
    
    return {"message": "Endereço atualizado com sucesso"}

def create_empresa_endereco(empresa_id: int, endereco: EmpresaEnderecoCreate, current_user: TokenPayLoad):
    # Verifica se o usuário é admin
    is_admin = "admin" in current_user.permissoes or "admin_master" in current_user.permissoes
    
    # Se NÃO for admin, o ID da empresa na URL DEVE ser o mesmo do token
    if not is_admin and current_user.empresa_id != empresa_id:
        raise HTTPException(
            status_code=403, 
            detail="Acesso negado: Você não tem permissão para criar um endereço para esta empresa."
        )

    # Se a verificação passar, o código continua
    novo_endereco = repo.create_endereco(empresa_id, endereco)
    return {"message": "Endereço criado com sucesso", "endereco": novo_endereco}

def delete_empresa_endereco(empresa_id: int):
    deleted = repo.repo_delete_endereco(empresa_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Nenhum endereço encontrado para esta empresa para ser removido.")
    return {"message": "Endereço removido com sucesso"}
