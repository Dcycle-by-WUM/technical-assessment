"""
Data models for the recommendation system.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class UserHistory:
    """
    Represents a user's browsing and purchase history.
    """
    user_id: str
    viewed_products: List[str]
    purchased_products: List[str]


@dataclass
class ProductCategory:
    """
    Represents a product category and its relationships.
    """
    name: str
    products: List[str]
    related_categories: List[str]


@dataclass
class BusinessRule:
    """
    Represents a business rule for filtering or modifying recommendations.
    """
    type: str
    factor: float = 1.0
    category: Optional[str] = None
    min_relevance: Optional[float] = None
    count: Optional[int] = None

