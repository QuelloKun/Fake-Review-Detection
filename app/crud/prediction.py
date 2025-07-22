from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.crud.base import CRUDBase
from app.models.prediction import Prediction
from app.api.v1.schemas.prediction import PredictionCreate, PredictionUpdate


class CRUDPrediction(CRUDBase[Prediction, PredictionCreate, PredictionUpdate]):
    async def get_user_predictions(
        self,
        db: AsyncSession,
        *,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Prediction]:
        statement = (
            select(Prediction)
            .where(Prediction.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(Prediction.created_at.desc())
        )
        result = await db.execute(statement)
        return result.scalars().all()

    async def get_stats(
        self,
        db: AsyncSession,
        *,
        user_id: Optional[str] = None,
    ) -> dict:
        statement = select(
            func.count(Prediction.id).label("total"),
            func.sum(
                func.case(
                    (Prediction.prediction_result == "real", 1),
                    else_=0,
                )
            ).label("real_count"),
            func.sum(
                func.case(
                    (Prediction.prediction_result == "fake", 1),
                    else_=0,
                )
            ).label("fake_count"),
            func.avg(Prediction.confidence_score).label("avg_confidence"),
        )

        if user_id:
            statement = statement.where(Prediction.user_id == user_id)

        result = await db.execute(statement)
        row = result.one()

        return {
            "total_predictions": row.total or 0,
            "real_reviews": row.real_count or 0,
            "fake_reviews": row.fake_count or 0,
            "average_confidence": float(row.avg_confidence) if row.avg_confidence else None,
        }

    async def create_with_user(
        self,
        db: AsyncSession,
        *,
        obj_in: PredictionCreate,
        user_id: Optional[str] = None,
    ) -> Prediction:
        db_obj = Prediction(
            **obj_in.model_dump(),
            user_id=user_id,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


prediction = CRUDPrediction(Prediction)
