from functools import lru_cache
from typing import Optional

from src.core.config import settings
from src.data.mongodb_repository import MongoDBRepository
from src.data.redis_cache import RedisCache
from src.services.recommendation_service import RecommendationService
from src.services.user_service import UserService
from src.services.product_service import ProductService
from src.algorithms.collaborative_filtering import CollaborativeFiltering
from src.algorithms.content_based import ContentBasedRecommender
from src.algorithms.hybrid_recommender import HybridRecommender


@lru_cache()
def get_mongodb_repository() -> MongoDBRepository:
    """
    Factory function for MongoDB repository with connection pooling.
    """
    return MongoDBRepository(
        connection_uri=settings.MONGODB_URI,
        database_name=settings.MONGODB_DB_NAME
    )


@lru_cache()
def get_redis_cache() -> RedisCache:
    """
    Factory function for Redis cache.
    """
    return RedisCache(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        ttl=settings.RECOMMENDATION_CACHE_TTL
    )


def get_recommendation_algorithm(version: Optional[str] = None):
    """
    Factory function for recommendation algorithm based on version.
    Allows for A/B testing different algorithm implementations.
    """
    version = version or settings.ALGORITHM_VERSION
    
    if version == "v1":
        return CollaborativeFiltering()
    elif version == "v2-beta":
        return HybridRecommender(
            collaborative_filtering=CollaborativeFiltering(),
            content_based=ContentBasedRecommender()
        )
    else:
        raise ValueError(f"Unknown algorithm version: {version}")


def get_user_service():
    """
    Factory function for user service.
    """
    return UserService(repository=get_mongodb_repository())


def get_product_service():
    """
    Factory function for product service.
    """
    return ProductService(repository=get_mongodb_repository())


def get_recommendation_service():
    """
    Factory function for recommendation service with all dependencies.
    """
    return RecommendationService(
        algorithm=get_recommendation_algorithm(),
        user_service=get_user_service(),
        product_service=get_product_service(),
        cache=get_redis_cache()
    )

