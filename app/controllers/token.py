from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, ValidationError
from typing import Optional, List
import jwt
from datetime import datetime, timedelta, timezone
import os

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "uma-chave-padrao-para-desenvolvimento")
if SECRET_KEY == "uma-chave-padrao-para-desenvolvimento":
    print("AVISO: Usando chave secreta de desenvolvimento. Defina a variável de ambiente SECRET_KEY em produção.")
ALGORITHM = "HS256"


class TokenPayLoad(BaseModel):
    """
    Define a estrutura de dados (payload) contida dentro do token JWT.
    """
    email: str
    # CORREÇÃO: O ID do usuário é uma string (UUID), não um inteiro.
    usuario_id: str
    empresa_id: Optional[int] = None
    permissoes: List[str] = []
    iat: int
    exp: int


def verificar_token(token: str) -> dict:
    """
    Decodifica e valida um token JWT.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


def gerar_token(email: str, usuario_id: str, permissoes: List[str], empresa_id: Optional[int] = None) -> str:
    """
    Gera um novo token JWT para um usuário.
    CORREÇÃO: A assinatura da função agora aceita usuario_id como string.
    """
    payload = {
        'email': email,
        'usuario_id': usuario_id,
        'empresa_id': empresa_id,
        'permissoes': permissoes,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(days=1),
    }
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Token gerado para o usuário {email}: {jwt_token}")
    return jwt_token


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenPayLoad:
    """
    Dependência FastAPI para obter o usuário atual a partir do token no header.
    """
    token = credentials.credentials
    try:
        payload = verificar_token(token)
        token_data = TokenPayLoad(**payload)
        return token_data
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token malformado ou com dados inválidos: {e.errors()}"
        )
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais"
        )


def require_permission(*permissoes_necessarias: str):
    """
    Fábrica de dependências para verificar permissões.
    """
    def permission_checker(current_user: TokenPayLoad = Depends(get_current_user)) -> dict:
        permissoes_usuario = set(current_user.permissoes)
        permissoes_requeridas = set(permissoes_necessarias)

        if "*" in permissoes_usuario or "admin_master" in permissoes_usuario:
            return current_user.model_dump()

        if permissoes_usuario.isdisjoint(permissoes_requeridas):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para executar esta ação."
            )
        return current_user.model_dump()

    return permission_checker
