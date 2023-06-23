from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID

from user.models import User


class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="E-mail Usuário")
    username: str = Field(
        ..., min_length=5, max_length=50, description="Nome de Usuário"
    )
    password: str = Field(
        ..., min_length=5, max_length=50, description="Senha do Usuário"
    )


class UserDetail(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: bool = False

    @staticmethod
    def from_user(user: User) -> "UserDetail":
        
        return UserDetail(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            disabled=user.disabled
        )
    