from typing import Optional
from user.schema import UserAuth, UserDetail
from user.models import User
from uuid import UUID
from core.security import get_password_hash, verify_password


class UserService:
    @staticmethod
    async def create_user(user: UserAuth) -> UserDetail:
        user = User(
            username=user.username,
            email=user.email,
            hash_password=get_password_hash(user.password),
        )
        await user.save()
        crated_user = UserDetail(**user.dict())

        return crated_user

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        return user

    @staticmethod
    async def get_user_by_id(id: UUID) -> Optional[User]:
        user = await User.find_one(User.id == id)
        return user

    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(
            password=password,
            hashed_password=user.hash_password,
        ):
            return None
        return user
