from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.security import verify_token
from app.crud import prediction as crud_prediction
from app.api.v1.schemas.prediction import (
    PredictionCreate,
    PredictionResponse,
    PredictionList,
    PredictionStats,
)
from app.services.ml_service import ml_service

router = APIRouter()


@router.post("/", response_model=PredictionResponse)
async def create_prediction(
    *,
    db: AsyncSession = Depends(deps.get_db),
    prediction_in: PredictionCreate,
    current_user_email: Optional[str] = Depends(verify_token),
) -> PredictionResponse:
    """Create a new prediction."""
    try:
        # Make prediction using ML service
        result, confidence = ml_service.predict(
            review_text=prediction_in.review_text,
            rating=prediction_in.rating,
            verified_purchase=prediction_in.verified_purchase,
            category=prediction_in.category,
        )
        
        # Create prediction record
        prediction = await crud_prediction.create_with_user(
            db,
            obj_in=prediction_in,
            user_id=current_user_email,
        )
        
        return PredictionResponse(
            id=prediction.id,
            user_id=prediction.user_id,
            review_text=prediction.review_text,
            rating=prediction.rating,
            verified_purchase=prediction.verified_purchase,
            category=prediction.category,
            prediction_result=result,
            confidence_score=confidence,
            model_version=prediction.model_version,
            created_at=prediction.created_at,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=PredictionList)
async def read_predictions(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user_email: Optional[str] = Depends(verify_token),
) -> PredictionList:
    """Get predictions for the current user."""
    if not current_user_email:
        # Return anonymous predictions
        predictions = await crud_prediction.get_multi(
            db, skip=skip, limit=limit
        )
        total = await crud_prediction.count(db)
    else:
        # Return user-specific predictions
        predictions = await crud_prediction.get_user_predictions(
            db, user_id=current_user_email, skip=skip, limit=limit
        )
        total = await crud_prediction.count(db, user_id=current_user_email)
    
    items = [
        PredictionResponse(
            id=prediction.id,
            user_id=prediction.user_id,
            review_text=prediction.review_text,
            rating=prediction.rating,
            verified_purchase=prediction.verified_purchase,
            category=prediction.category,
            prediction_result=prediction.prediction_result,
            confidence_score=prediction.confidence_score,
            model_version=prediction.model_version,
            created_at=prediction.created_at,
        )
        for prediction in predictions
    ]
    
    pages = (total + limit - 1) // limit
    
    return PredictionList(
        items=items,
        total=total,
        page=skip // limit + 1,
        size=len(items),
        pages=pages,
    )


@router.get("/stats", response_model=PredictionStats)
async def get_prediction_stats(
    db: AsyncSession = Depends(deps.get_db),
    current_user_email: Optional[str] = Depends(verify_token),
) -> PredictionStats:
    """Get prediction statistics."""
    stats = await crud_prediction.get_stats(
        db, user_id=current_user_email
    )
    
    return PredictionStats(**stats)


@router.get("/{prediction_id}", response_model=PredictionResponse)
async def read_prediction(
    prediction_id: str,
    db: AsyncSession = Depends(deps.get_db),
    current_user_email: Optional[str] = Depends(verify_token),
) -> PredictionResponse:
    """Get a specific prediction."""
    prediction = await crud_prediction.get(db, id=prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    # Check if user owns this prediction
    if current_user_email and str(prediction.user_id) != str(current_user_email):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return PredictionResponse(
        id=prediction.id,
        user_id=prediction.user_id,
        review_text=prediction.review_text,
        rating=prediction.rating,
        verified_purchase=prediction.verified_purchase,
        category=prediction.category,
        prediction_result=prediction.prediction_result,
        confidence_score=prediction.confidence_score,
        model_version=prediction.model_version,
        created_at=prediction.created_at,
    )
