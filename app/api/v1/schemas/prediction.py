from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class PredictionBase(BaseModel):
    review_text: str = Field(..., min_length=1, max_length=5000)
    rating: int = Field(..., ge=1, le=5)
    verified_purchase: bool
    category: str = Field(..., min_length=1, max_length=100)


class PredictionCreate(PredictionBase):
    pass


class PredictionUpdate(BaseModel):
    review_text: Optional[str] = Field(None, min_length=1, max_length=5000)
    rating: Optional[int] = Field(None, ge=1, le=5)
    verified_purchase: Optional[bool] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    prediction_result: Optional[str] = None
    confidence_score: Optional[float] = None
    model_version: Optional[str] = None


class PredictionResponse(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    review_text: str
    rating: int
    verified_purchase: bool
    category: str
    prediction_result: str
    confidence_score: Optional[float] = None
    model_version: str
    created_at: datetime

    class Config:
        from_attributes = True


class PredictionList(BaseModel):
    items: list[PredictionResponse]
    total: int
    page: int
    size: int
    pages: int


class PredictionStats(BaseModel):
    total_predictions: int
    real_reviews: int
    fake_reviews: int
    average_confidence: Optional[float] = None
