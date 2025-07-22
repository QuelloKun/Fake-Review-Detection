from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_token
from app.db.session import get_db as get_database_session

security = HTTPBearer(auto_error=False)


async def get_db() -> AsyncSession:
    async for session in get_database_session():
        yield session


async def get_current_user_email(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[str]:
    """Get current user email from JWT token."""
    if credentials is None:
        return None
    
    token = credentials.credentials
    email = verify_token(token)
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return email


async def get_current_active_user(
    current_user_email: str = Depends(get_current_user_email),
) -> str:
    """Get current active user."""
    if current_user_email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return current_user_email
