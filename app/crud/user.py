from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.user import User
from app.api.v1.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        from app.core.security import get_password_hash
        
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self, db: AsyncSession, *, email: str, password: str
    ) -> Optional[User]:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        from app.core.security import verify_password
        if not verify_password(password, user.hashed_password):
            return None
        return user


user = CRUDUser(User)
