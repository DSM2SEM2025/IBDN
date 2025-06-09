from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional


import jwt
from datetime import datetime, timedelta, timezone

security = HTTPBearer()

SECRET_KEY = "chave-muito-secreta"
ALGORITHM = "HS256"


class TokenPayLoad(BaseModel):
    email: str
    permissoes: Optional[str] = None
    empresa_id: Optional[int] = None
    iat: int
    exp: int


def verificar_token(token) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


def gerar_token(email: str, permissoes: str, usuario_id: Optional[int] = None) -> str:
    payload = {
        'email': email,
        'usuario_id': usuario_id,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(days=1),
        "permissoes": permissoes,
    }
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Token gerado para o usuário {email}: {jwt_token}")
    return jwt_token


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = verificar_token(token)
        token_data = TokenPayLoad(**payload)
        return token_data
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais"
        )
