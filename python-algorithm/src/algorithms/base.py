from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class RecommendationAlgorithm(ABC):
    """
    Base abstract class for recommendation algorithms.
    """
    
    @property
    def version(self) -> str:
        """Get the algorithm version."""
        return "base"
    
    @abstractmethod
    def generate_recommendations(
        self,
        user_data: Dict[str, Any],
        user_history: List[Dict[str, Any]],
        candidate_products: List[Dict[str, Any]],
        context: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generate product recommendations for a user.
        
        Args:
            user_data: User profile data
            user_history: User interaction history
            candidate_products: List of candidate products
            context: Optional context information
            
        Returns:
            A list of product recommendations with scores
        """
        pass
    
    def update_model_incrementally(
        self, user_id: str, product_id: str, interaction_type: str
    ) -> None:
        """
        Update the recommendation model incrementally with new user interaction.
        
        Args:
            user_id: The ID of the user
            product_id: The ID of the product
            interaction_type: The type of interaction
            
        Raises:
            NotImplementedError: If the algorithm doesn't support incremental updates
        """
        raise NotImplementedError("Incremental updates not supported by this algorithm")
    
    def train_model(
        self,
        user_data: List[Dict[str, Any]],
        product_data: List[Dict[str, Any]],
        interaction_data: List[Dict[str, Any]],
    ) -> None:
        """
        Train the recommendation model from scratch.
        
        Args:
            user_data: List of user profiles
            product_data: List of product data
            interaction_data: List of user-product interactions
            
        Raises:
            NotImplementedError: If the algorithm doesn't support full training
        """
        raise NotImplementedError("Full model training not supported by this algorithm")
    
    def evaluate_model(
        self,
        test_data: List[Dict[str, Any]],
    ) -> Dict[str, float]:
        """
        Evaluate the recommendation model on test data.
        
        Args:
            test_data: Test dataset for evaluation
            
        Returns:
            A dictionary of evaluation metrics
            
        Raises:
            NotImplementedError: If the algorithm doesn't support evaluation
        """
        raise NotImplementedError("Model evaluation not supported by this algorithm")

