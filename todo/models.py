from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document, Indexed, Link, before_event, Replace, Insert
from pydantic import Field
from user.models import User


class Todo(Document):
    id: UUID = Field(default_factory=uuid4, unique=True, alias="_id")
    status: bool = False
    title: Indexed(str)
    description: Indexed(str)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    owner: Link[User]
    
    
    def __repr__(self) -> str:
        return f'<Todo {self.title}>'
    

    def __str__(self) -> str:
        return self.title
    
    
    def __hash__(self) -> int:
        return hash(self.title)
    
    
    def __eq__(self, o: object) -> bool:
        if isinstance(o, Todo):
            return self.id == o.id
        return False
    
    
    @before_event([Replace, Insert])
    def sync_update_at(self):
        self.updated_at = datetime.utcnow()
