from fastapi import APIRouter, Depends
from todo.schema import TodoDetail
from user.models import User
from user.deps import get_current_user

todo_router = APIRouter()

@todo_router.get('/', summary='Lista Todas as Notas', response_model=TodoDetail)
async def list(current_user: User = Depends(get_current_user)):
    return current_user