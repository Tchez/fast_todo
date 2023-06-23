from api.auth.schema import TokenPayload
from core.config import settings
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from .services import UserService
from .models import User

auth_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    scheme_name="JWT",
)


async def get_current_user(token: str = Depends(auth_scheme)) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            settings.ALGORITHM,
        )
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token foi expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except (ValidationError, jwt.JWTError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Erro na validação do token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await UserService.get_user_by_id(token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
