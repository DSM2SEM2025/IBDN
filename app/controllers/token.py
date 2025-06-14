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
    usuario_id: Optional[int] = None
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


def gerar_token(email: str, permissoes: list, usuario_id: Optional[int] = None) -> str:
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


def require_permission(*permissoes_necessarias: str):
    """
    Fábrica de dependências que aceita MÚLTIPLAS permissões e verifica 
    se o usuário possui PELO MENOS UMA delas.

    Args:
        *permissoes_necessarias (str): Uma ou mais strings de permissão.
                                        Ex: require_permission("admin", "empresa")
    """
    def permission_checker(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
        token = credentials.credentials
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            permissoes_usuario = payload.get("permissoes", []) # Esta é a LISTA de permissões do usuário

            if not isinstance(permissoes_usuario, list):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Formato de permissões inválido no token."
                )

            # --- A LÓGICA DO 'IF' CORRIGIDA PARA LISTAS ---

            # 1. Checa se o usuário é um super admin com permissão coringa ("*")
            if "*" in permissoes_usuario:
                return payload # Se for, libera o acesso imediatamente.

            # 2. Converte as duas listas para 'sets' para uma verificação eficiente.
            permissoes_usuario_set = set(permissoes_usuario)
            # 'permissoes_necessarias' aqui é um tuple, ex: ("admin", "empresa")
            permissoes_necessarias_set = set(permissoes_necessarias)

            # 3. O 'if' agora checa se não há NENHUM item em comum entre os dois sets.
            #    A função .isdisjoint() faz exatamente isso e é muito rápida.
            if permissoes_usuario_set.isdisjoint(permissoes_necessarias_set):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Você não tem permissão para executar esta ação."
                )
            
            # Se chegou até aqui, o usuário tem pelo menos uma das permissões necessárias.
            return payload

        except (jwt.PyJWTError, AttributeError):
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não foi possível validar as credenciais.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    return permission_checker