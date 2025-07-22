from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.api.v1.endpoints import auth, predictions, health
from app.api.v1.schemas.prediction import PredictionCreate
from app.crud import prediction as crud_prediction
from app.api import deps
from app.db.base import Base
from app.db.session import engine
from app.services.ml_service import ml_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["authentication"],
)
app.include_router(
    predictions.router,
    prefix=f"{settings.API_V1_STR}/predictions",
    tags=["predictions"],
)
app.include_router(
    health.router,
    prefix=f"{settings.API_V1_STR}/health",
    tags=["health"],
)


# Legacy prediction endpoint for frontend compatibility
@app.post("/predict", response_class=HTMLResponse)
async def predict_frontend(
    request: Request,
    news: str = Form(...),
    rating: int = Form(...),
    verified_options: str = Form(...),
    category_options: str = Form(...),
    db: AsyncSession = Depends(deps.get_db)
):
    """Handle frontend prediction form submission and save to database."""
    try:
        # Make prediction using ML service
        result, confidence = ml_service.predict(
            review_text=news,
            rating=rating,
            verified_purchase=verified_options == "Y",
            category=category_options,
        )
        
        # Create prediction object for database with all data
        from app.models.prediction import Prediction
        import uuid
        from datetime import datetime
        
        saved_prediction = Prediction(
            id=uuid.uuid4(),
            user_id=None,  # Anonymous frontend submission
            review_text=news,
            rating=rating,
            verified_purchase=verified_options == "Y",
            category=category_options,
            prediction_result=result,
            confidence_score=confidence,
            model_version="1.0.0",
            created_at=datetime.utcnow()
        )
        
        # Save to database
        db.add(saved_prediction)
        await db.commit()
        await db.refresh(saved_prediction)
        
        # Return simple HTML response for Next.js frontend
        return f"Review is {result.title()}"
        
    except Exception as e:
        return f"Error: {str(e)}"


# API Root endpoint
@app.get("/")
async def api_root():
    """API root endpoint."""
    return {"message": "Fake Review Detection API", "version": settings.VERSION}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
