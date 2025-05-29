from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from src.core.dependencies import get_recommendation_service
from src.core.monitoring import track_request
from src.services.recommendation_service import RecommendationService

router = APIRouter()


class ProductRecommendation(BaseModel):
    product_id: str
    score: float
    rank: int
    features: Optional[List[str]] = None


class RecommendationResponse(BaseModel):
    user_id: str
    recommendations: List[ProductRecommendation]
    algorithm_version: str
    context: Optional[str] = None


@router.get("/{user_id}", response_model=RecommendationResponse)
@track_request
async def get_recommendations(
    user_id: str,
    limit: int = Query(10, ge=1, le=100),
    algorithm_version: Optional[str] = None,
    category: Optional[str] = None,
    context: Optional[str] = None,
    recommendation_service: RecommendationService = Depends(get_recommendation_service),
):
    """
    Get personalized product recommendations for a user.
    
    - **user_id**: The ID of the user to get recommendations for
    - **limit**: Maximum number of recommendations to return
    - **algorithm_version**: Optional specific algorithm version to use
    - **category**: Optional category filter for recommendations
    - **context**: Optional context information (e.g., "homepage", "cart", "product_page")
    """
    try:
        recommendations = recommendation_service.get_recommendations_for_user(
            user_id=user_id,
            limit=limit,
            algorithm_version=algorithm_version,
            category=category,
            context=context,
        )
        
        # Convert to response model
        return RecommendationResponse(
            user_id=user_id,
            recommendations=[
                ProductRecommendation(
                    product_id=rec["product_id"],
                    score=rec["score"],
                    rank=idx + 1,
                    features=rec.get("features"),
                )
                for idx, rec in enumerate(recommendations)
            ],
            algorithm_version=algorithm_version or recommendation_service.get_current_algorithm_version(),
            context=context,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")


@router.post("/{user_id}/feedback")
async def record_recommendation_feedback(
    user_id: str,
    product_id: str,
    interaction_type: str = Query(..., description="Type of interaction: click, view, purchase, etc."),
    recommendation_service: RecommendationService = Depends(get_recommendation_service),
):
    """
    Record user feedback on recommendations for continuous improvement.
    
    - **user_id**: The ID of the user providing feedback
    - **product_id**: The product ID the user interacted with
    - **interaction_type**: The type of interaction (click, view, purchase, etc.)
    """
    try:
        recommendation_service.record_user_feedback(
            user_id=user_id,
            product_id=product_id,
            interaction_type=interaction_type,
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record feedback: {str(e)}")


@router.post("/batch")
async def trigger_batch_recommendations(
    recommendation_service: RecommendationService = Depends(get_recommendation_service),
):
    """
    Trigger a batch recommendation generation job.
    This endpoint is typically called by a scheduled job.
    """
    try:
        job_id = recommendation_service.trigger_batch_recommendation_job()
        return {"status": "success", "job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger batch job: {str(e)}")


@router.get("/batch/{job_id}/status")
async def get_batch_job_status(
    job_id: str,
    recommendation_service: RecommendationService = Depends(get_recommendation_service),
):
    """
    Get the status of a batch recommendation job.
    """
    try:
        status = recommendation_service.get_batch_job_status(job_id)
        return {"job_id": job_id, "status": status}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get job status: {str(e)}")

