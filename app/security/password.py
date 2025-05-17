from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_senha(senha: str, hashed_senha: str) -> bool:
    print(hashed_senha, senha)
    return pwd_context.verify(senha, hashed_senha)
