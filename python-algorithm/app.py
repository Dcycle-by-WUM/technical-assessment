import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.api import router as api_router
from src.core.config import settings
from src.core.dependencies import get_recommendation_service
from src.core.monitoring import setup_monitoring, track_request
from src.services.recommendation_service import RecommendationService

app = FastAPI(
    title="Recommendation Engine API",
    description="Product recommendation engine for e-commerce platform",
    version="0.1.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Security concern: too permissive for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup monitoring
setup_monitoring(app)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Example direct usage of service in API - architectural concern
@app.get("/quick-recommendations/{user_id}")
@track_request
async def quick_recommendations(
    user_id: str, recommendation_service: RecommendationService = Depends(get_recommendation_service)
):
    try:
        recommendations = recommendation_service.get_recommendations_for_user(user_id, limit=5)
        return {"user_id": user_id, "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Development server configuration
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )

