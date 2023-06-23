import pymongo
from fastapi import APIRouter, HTTPException, status, Depends
from user.schema import UserAuth, UserDetail
from user.services import UserService
from user.models import User
from user.deps import get_current_user


user_router = APIRouter()


@user_router.post("/adiciona", summary="Adiciona um novo usuário", response_model=UserDetail)
async def add_user(data: UserAuth):
    try:
        return await UserService.create_user(data)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já existe",
        )
        
@user_router.get("/me", summary="Detalhes do usuário logado", response_model=UserDetail)
async def get_user(user: User = Depends(get_current_user)):
    return UserDetail.from_user(user)