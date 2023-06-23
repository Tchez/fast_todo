from core.security import create_access_token, create_refresh_token
from fastapi import Depends, APIRouter, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from .schema import TokenSchema, TokenPayload
from typing import Any
from user.deps import get_current_user
from user.models import User
from user.services import UserService
from user.schema import UserDetail
from pydantic import ValidationError
from core.config import settings
from jose import jwt

auth_router = APIRouter()


@auth_router.post(
    "/login", summary="Cria um access token e refresh token", response_model=TokenSchema
)
async def login(data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate_user(
        email=data.username,
        password=data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
        )

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }


@auth_router.post(
    "/test-token", summary="Testa um access token", response_model=UserDetail
)
async def test_token(current_user: User = Depends(get_current_user)):
    return UserDetail.from_user(current_user)


@auth_router.post('/refresh-token', summary='Refresh Token', response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            settings.ALGORITHM,
        )
        token_data = TokenPayload(**payload)      
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = await UserService.get_user_by_id(token_data.sub)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {            
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }