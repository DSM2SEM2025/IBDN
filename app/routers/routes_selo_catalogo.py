# app/routers/routes_selo_catalogo.py
from fastapi import APIRouter, Depends, status
from typing import List
from app.controllers import controller_selo as ctrl
from app.models.selo_model import SeloInDB, SeloCreate, SeloUpdate
from app.controllers.token import require_permission

router = APIRouter(
    prefix="/selos-catalogo",
    tags=["Catálogo de Selos"],
    # Estas rotas são apenas para administradores gerirem os tipos de selo
    dependencies=[Depends(require_permission("admin", "admin_master"))],
    responses={404: {"description": "Não encontrado"}},
)


@router.post("/", response_model=SeloInDB, status_code=status.HTTP_201_CREATED, summary="Cria um novo tipo de selo no catálogo")
def criar_selo_no_catalogo(data: SeloCreate):
    """
    Cria um novo tipo de selo que estará disponível para ser concedido às empresas.
    Apenas administradores podem executar esta ação.
    """
    return ctrl.criar_tipo_selo(data)


@router.get("/", response_model=List[SeloInDB], summary="Lista todos os tipos de selo do catálogo")
def listar_selos_do_catalogo():
    """
    Retorna uma lista de todos os tipos de selo disponíveis no sistema.
    """
    return ctrl.listar_tipos_selo()

# NOTA: Rotas para PUT e DELETE para o catálogo podem ser adicionadas aqui, seguindo o mesmo padrão.
# Por exemplo:
# @router.put("/{id_selo}", response_model=SeloInDB)
# def atualizar_selo_no_catalogo(id_selo: int, data: SeloUpdate):
#     # ... chamar a função correspondente no controller
#     pass
