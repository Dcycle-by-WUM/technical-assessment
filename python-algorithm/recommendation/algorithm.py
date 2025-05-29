"""
Implementation of the recommendation algorithm.

This module contains the main algorithm for generating product recommendations
based on user browsing history, product categories, and business rules.
"""
from typing import List, Dict, Any
import logging

from recommendation.models import UserHistory, ProductCategory, BusinessRule

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_recommendations(
    user_history: UserHistory,
    product_categories: List[ProductCategory],
    business_rules: List[BusinessRule],
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Generate personalized product recommendations for a user.
    
    Args:
        user_history: The user's browsing and purchase history
        product_categories: List of product categories and their relationships
        business_rules: List of business rules to apply to recommendations
        limit: Maximum number of recommendations to return
        
    Returns:
        A list of recommended products with relevance scores
    """
    logger.info(f"Generating recommendations for user {user_history.user_id}")
    
    # TODO: Implement the recommendation algorithm
    # This is where you will implement your solution for the challenge
    
    # Placeholder implementation that returns random products
    # Replace this with your actual algorithm implementation
    import random
    
    # Get all products
    all_products = []
    for category in product_categories:
        all_products.extend(category.products)
    
    # Remove products the user has already purchased
    candidate_products = [p for p in all_products if p not in user_history.purchased_products]
    
    # Sort by "relevance" (random for this placeholder)
    recommendations = [
        {
            "product_id": product,
            "relevance_score": round(random.random(), 2),
            "reason": "Placeholder recommendation"
        }
        for product in candidate_products
    ]
    
    # Sort by relevance score (descending)
    recommendations.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    # Apply limit
    recommendations = recommendations[:limit]
    
    logger.info(f"Generated {len(recommendations)} recommendations")
    return recommendations

