import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    review_text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    verified_purchase = Column(Boolean, nullable=False)
    category = Column(String(100), nullable=False)
    prediction_result = Column(String(10), nullable=False)  # 'real' or 'fake'
    confidence_score = Column(Float, nullable=True)
    model_version = Column(String(50), default="1.0.0")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="predictions")
