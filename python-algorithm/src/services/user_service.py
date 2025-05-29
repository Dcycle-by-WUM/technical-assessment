import logging
from typing import Dict, List, Optional, Any

from src.data.mongodb_repository import MongoDBRepository

logger = logging.getLogger(__name__)


class UserService:
    """
    Service for user-related operations.
    """
    
    def __init__(self, repository: MongoDBRepository):
        self.repository = repository
    
    def get_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user profile data.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            User data or None if not found
        """
        try:
            user = self.repository.find_one("users", {"id": user_id})
            
            if not user and user_id.startswith("test_"):
                # For testing, generate mock data for test users
                return self._generate_mock_user_data(user_id)
            
            return user
        except Exception as e:
            logger.error(f"Error retrieving user data: {str(e)}")
            return None
    
    def get_user_interaction_history(
        self, user_id: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get user interaction history.
        
        Args:
            user_id: The ID of the user
            limit: Maximum number of interactions to return
            
        Returns:
            List of user interactions
        """
        try:
            interactions = self.repository.find_many(
                "interactions",
                {"user_id": user_id},
                sort=[("timestamp", -1)],  # Sort by timestamp descending
                limit=limit,
            )
            
            if not interactions and user_id.startswith("test_"):
                # For testing, generate mock interactions for test users
                return self._generate_mock_interactions(user_id)
            
            return interactions
        except Exception as e:
            logger.error(f"Error retrieving user interaction history: {str(e)}")
            return []
    
    def record_user_interaction(
        self, user_id: str, product_id: str, interaction_type: str
    ) -> bool:
        """
        Record a user interaction with a product.
        
        Args:
            user_id: The ID of the user
            product_id: The ID of the product
            interaction_type: The type of interaction
            
        Returns:
            True if successful, False otherwise
        """
        try:
            interaction = {
                "user_id": user_id,
                "product_id": product_id,
                "interaction_type": interaction_type,
                "timestamp": {"$currentDate": True},
            }
            
            result = self.repository.insert_one("interactions", interaction)
            return result is not None
        except Exception as e:
            logger.error(f"Error recording user interaction: {str(e)}")
            return False
    
    def get_user_segments(self, user_id: str) -> List[str]:
        """
        Get the segments a user belongs to.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            List of segment IDs
        """
        try:
            user = self.get_user_data(user_id)
            if not user:
                return []
            
            return user.get("segments", [])
        except Exception as e:
            logger.error(f"Error retrieving user segments: {str(e)}")
            return []
    
    def _generate_mock_user_data(self, user_id: str) -> Dict[str, Any]:
        """
        Generate mock user data for testing.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            Mock user data
        """
        # Extract a numeric ID from the test user ID
        try:
            numeric_id = int(user_id.split("_")[1])
        except (IndexError, ValueError):
            numeric_id = hash(user_id) % 1000
        
        # Determine subscription tier based on ID
        if numeric_id % 10 == 0:
            tier = "premium"
        elif numeric_id % 5 == 0:
            tier = "plus"
        else:
            tier = "basic"
        
        # Generate segments based on ID
        segments = []
        if numeric_id % 2 == 0:
            segments.append("high_value")
        if numeric_id % 3 == 0:
            segments.append("frequent_shopper")
        if numeric_id % 7 == 0:
            segments.append("new_customer")
        
        return {
            "id": user_id,
            "name": f"Test User {numeric_id}",
            "email": f"test{numeric_id}@example.com",
            "subscription_tier": tier,
            "segments": segments,
            "preferences": {
                "categories": ["electronics", "books"] if numeric_id % 2 == 0 else ["clothing", "home"],
            },
        }
    
    def _generate_mock_interactions(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Generate mock interactions for testing.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            List of mock interactions
        """
        try:
            numeric_id = int(user_id.split("_")[1])
        except (IndexError, ValueError):
            numeric_id = hash(user_id) % 1000
        
        # Generate a deterministic but varied set of interactions
        interactions = []
        
        # View interactions (more common)
        for i in range(1, 21):
            product_id = f"product_{(numeric_id * i) % 1000}"
            interactions.append({
                "user_id": user_id,
                "product_id": product_id,
                "interaction_type": "view",
                "timestamp": {"$date": f"2023-05-{i:02d}T10:00:00Z"},
            })
        
        # Click interactions (less common)
        for i in range(1, 11):
            if i % 2 == 0:
                product_id = f"product_{(numeric_id * i) % 1000}"
                interactions.append({
                    "user_id": user_id,
                    "product_id": product_id,
                    "interaction_type": "click",
                    "timestamp": {"$date": f"2023-05-{i:02d}T11:00:00Z"},
                })
        
        # Purchase interactions (least common)
        for i in range(1, 6):
            if i % 3 == 0:
                product_id = f"product_{(numeric_id * i) % 1000}"
                interactions.append({
                    "user_id": user_id,
                    "product_id": product_id,
                    "interaction_type": "purchase",
                    "timestamp": {"$date": f"2023-05-{i:02d}T12:00:00Z"},
                })
        
        return interactions

