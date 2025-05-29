from fastapi import APIRouter

from src.api.v1.endpoints import recommendations, users, products, health

router = APIRouter()

router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(products.router, prefix="/products", tags=["products"])
router.include_router(health.router, prefix="/health", tags=["health"])

