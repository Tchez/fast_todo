from beanie import Document, Indexed
from uuid import uuid4, UUID
from pydantic import EmailStr, Field
from datetime import datetime
from typing import Optional


class User(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    hash_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: bool = False

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return self.email

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False

    @property
    def create(self) -> datetime:
        return self.id.generation_time

    @classmethod
    async def by_email(self, email: str) -> "User":
        return await User.find_one(self.email == email)
