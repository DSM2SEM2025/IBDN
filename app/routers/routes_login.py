import asyncio
from fastapi import APIRouter, HTTPException
from fastapi import APIRouter, HTTPException, status

from app.models.usuario_model import UsuarioResponse, CredenciaisLogin
from app.controllers.controller_login import login
router = APIRouter(
    prefix="",
    tags=["login"],
    responses={404: {"description": "Não encontrado"}},
)


@router.post("/login", summary="Login de usuário")
async def login_usuario(request: CredenciaisLogin):
    resultado = login(request.email, request.senha)
    print(request)
    print(
        f"Tipo da  função login: {type(login)}, is coroutine? {asyncio.iscoroutinefunction(login)}")

    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {
        "message": "Login bem-sucedido",
        "token": resultado
    }
