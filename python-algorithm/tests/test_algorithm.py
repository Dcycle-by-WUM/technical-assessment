"""
Tests for the recommendation algorithm.
"""
import pytest
from recommendation.algorithm import generate_recommendations
from recommendation.models import UserHistory, ProductCategory, BusinessRule


def test_generate_recommendations_basic():
    """Test basic recommendation generation."""
    # Test data
    user_history = UserHistory(
        user_id="test_user",
        viewed_products=["product1", "product2"],
        purchased_products=["product3"]
    )
    
    product_categories = [
        ProductCategory(
            name="electronics",
            products=["product1", "product3", "product4"],
            related_categories=["home"]
        ),
        ProductCategory(
            name="home",
            products=["product2", "product5"],
            related_categories=["electronics"]
        )
    ]
    
    business_rules = [
        BusinessRule(type="boost", category="electronics", factor=1.2),
        BusinessRule(type="filter", min_relevance=0.3)
    ]
    
    # Generate recommendations
    recommendations = generate_recommendations(
        user_history=user_history,
        product_categories=product_categories,
        business_rules=business_rules,
        limit=3
    )
    
    # Basic assertions
    assert isinstance(recommendations, list)
    assert len(recommendations) <= 3
    
    # Check structure of recommendations
    for rec in recommendations:
        assert "product_id" in rec
        assert "relevance_score" in rec
        assert "reason" in rec
        
        # Make sure we're not recommending products the user already purchased
        assert rec["product_id"] not in user_history.purchased_products


def test_generate_recommendations_empty_history():
    """Test recommendation generation with empty history."""
    # Test data
    user_history = UserHistory(
        user_id="new_user",
        viewed_products=[],
        purchased_products=[]
    )
    
    product_categories = [
        ProductCategory(
            name="electronics",
            products=["product1", "product3", "product4"],
            related_categories=[]
        )
    ]
    
    business_rules = []
    
    # Generate recommendations
    recommendations = generate_recommendations(
        user_history=user_history,
        product_categories=product_categories,
        business_rules=business_rules,
        limit=5
    )
    
    # Assertions
    assert isinstance(recommendations, list)
    assert len(recommendations) <= 5


# TODO: Add more tests for specific algorithm functionality
# These would test:
# - Behavior with different business rules
# - Correct application of category relationships
# - Performance with larger datasets
# - Edge cases and error handling

