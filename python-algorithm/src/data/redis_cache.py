import json
import logging
from typing import Any, Dict, List, Optional, Union

import redis

from src.core.monitoring import track_cache

logger = logging.getLogger(__name__)


class RedisCache:
    """
    Redis cache implementation for storing and retrieving recommendation data.
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        password: Optional[str] = None,
        ttl: int = 3600,  # Default TTL: 1 hour
    ):
        try:
            self.client = redis.Redis(
                host=host,
                port=port,
                password=password,
                decode_responses=False,  # We'll handle JSON decoding ourselves
                socket_timeout=5.0,  # Timeout for Redis operations
                socket_connect_timeout=5.0,
                health_check_interval=30,
            )
            self.ttl = ttl
            self.enabled = True
            
            # Test connection
            self.client.ping()
            logger.info("Redis cache initialized successfully")
            
        except redis.ConnectionError as e:
            logger.warning(f"Failed to connect to Redis: {str(e)}. Cache disabled.")
            self.enabled = False
    
    @track_cache(cache_type="recommendations")
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        if not self.enabled:
            return None
        
        try:
            value = self.client.get(key)
            if value is None:
                return None
            
            return json.loads(value)
        except (redis.RedisError, json.JSONDecodeError) as e:
            logger.error(f"Error retrieving from cache: {str(e)}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (optional)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            serialized_value = json.dumps(value)
            return self.client.set(
                key, serialized_value, ex=(ttl or self.ttl)
            )
        except (redis.RedisError, TypeError) as e:
            logger.error(f"Error setting cache: {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete a key from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            return bool(self.client.delete(key))
        except redis.RedisError as e:
            logger.error(f"Error deleting from cache: {str(e)}")
            return False
    
    def delete_pattern(self, pattern: str) -> int:
        """
        Delete all keys matching a pattern.
        
        Args:
            pattern: Pattern to match (e.g., "user:123:*")
            
        Returns:
            Number of keys deleted
        """
        if not self.enabled:
            return 0
        
        try:
            # SCAN is more efficient for large datasets than KEYS
            cursor = 0
            deleted_count = 0
            
            while True:
                cursor, keys = self.client.scan(cursor, match=pattern, count=100)
                if keys:
                    deleted_count += self.client.delete(*keys)
                
                if cursor == 0:
                    break
            
            return deleted_count
        except redis.RedisError as e:
            logger.error(f"Error deleting pattern from cache: {str(e)}")
            return 0
    
    def clear_all(self) -> bool:
        """
        Clear the entire cache.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            return self.client.flushdb()
        except redis.RedisError as e:
            logger.error(f"Error clearing cache: {str(e)}")
            return False

