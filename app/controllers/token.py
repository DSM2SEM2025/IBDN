from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


import jwt
from datetime import datetime, timedelta, timezone

security = HTTPBearer()

SECRET_KEY = "chave-muito-secreta"
ALGORITHM = "HS256"


def verificar_token(token) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY,
                             algorithms=[ALGORITM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


def gerar_token(email: str, tipo_usuario: str) -> str:
    payload = {
        'email': email,
        'tipo_usuario': tipo_usuario,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(days=1)}
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = verificar_token(token)
        exp = payload.get('exp')
        if exp and datetime.fromtimestamp(exp) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Erro inesperado ao verificar token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar autenticação",
            headers={"WWW-Authenticate": "Bearer"},
        )
