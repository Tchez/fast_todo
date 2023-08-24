import bson
from todo.models import Todo
from todo.schema import TodoCreate, TodoDetail, TodoUpdate
from typing import List
from uuid import UUID, uuid4
from user.models import User


class TodoService:
    @staticmethod
    async def list_todos(user: User) -> List[Todo]:
        todos = await Todo.find(Todo.owner.id == user.id).to_list()
        for todo in todos:
            todo.id = UUID(bytes=todo.id.binary)
        return todos


    
    @staticmethod
    async def create_todo(user: User, data: TodoCreate) -> Todo:
        todo = Todo(
            **data.dict(), 
            owner=user.id,
        )
        
        return await todo.insert()