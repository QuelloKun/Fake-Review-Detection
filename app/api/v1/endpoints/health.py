from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.api import deps
from app.services.ml_service import ml_service

router = APIRouter()


@router.get("/")
async def health_check(
    db: AsyncSession = Depends(deps.get_db),
) -> dict:
    """Health check endpoint."""
    health_status = {
        "status": "healthy",
        "database": "connected",
        "model": "loaded" if ml_service.health_check() else "failed",
    }
    
    # Test database connection
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        health_status["database"] = "disconnected"
        health_status["status"] = "unhealthy"
    
    return health_status


@router.get("/ready")
async def readiness_check(
    db: AsyncSession = Depends(deps.get_db),
) -> dict:
    """Readiness check for Kubernetes."""
    checks = {
        "database": False,
        "model": False,
    }
    
    # Check database
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = True
    except Exception:
        pass
    
    # Check model
    checks["model"] = ml_service.health_check()
    
    ready = all(checks.values())
    
    return {
        "ready": ready,
        "checks": checks,
    }
