from fastapi import APIRouter, Depends
from todo.models import Todo
from todo.schema import TodoDetail, TodoCreate
from todo.services import TodoService
from typing import List
from user.models import User
from user.deps import get_current_user

todo_router = APIRouter()

@todo_router.get('/', summary='Lista Todas as Notas', response_model=TodoDetail)
async def list(current_user: User = Depends(get_current_user)):
    return await TodoService.list_todos(current_user)


@todo_router.post('/', summary='Cria uma nova Nota', response_model=Todo)
async def create_todo(
    data: TodoCreate,
    current_user: User = Depends(get_current_user)
):
    return await TodoService.create_todo(
        current_user,
        data
    )
