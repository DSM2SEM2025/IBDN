from fastapi import APIRouter, HTTPException

from app.models.usuario_model import UsuarioResponse, CredenciaisLogin
from app.controllers.controller_login import login
router = APIRouter(
    prefix="",
    tags=["login"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post("/login",     summary="Login de usuário")
async def login_usuario(request: CredenciaisLogin):
    resultado = await login(request.email, request.senha)
    if resultado:
        return {"message": "Login bem-sucedido", "token": resultado}
    else:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
