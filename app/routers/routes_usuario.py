from fastapi import APIRouter

from app.models.usuario_model import UsuarioResponse, CredenciaisLogin
from app.controllers.controller_usuario import login
router = APIRouter(
    prefix="",
    tags=["Usuários"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post("/usuarios/login",     summary="Login de usuário")
async def login_usuario(request: CredenciaisLogin):
    resultado = await login(request.email, request.senha)
    return resultado
