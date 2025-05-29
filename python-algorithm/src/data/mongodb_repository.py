import logging
from typing import Any, Dict, List, Optional, Union

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import PyMongoError
from pymongo.collection import Collection

logger = logging.getLogger(__name__)


class MongoDBRepository:
    """
    MongoDB repository for storing and retrieving recommendation-related data.
    """
    
    def __init__(
        self,
        connection_uri: str = "mongodb://localhost:27017",
        database_name: str = "recommendation_engine",
    ):
        try:
            # Create MongoDB client with connection pooling
            self.client = MongoClient(
                connection_uri,
                maxPoolSize=50,  # Connection pool size
                connectTimeoutMS=5000,  # Connection timeout
                serverSelectionTimeoutMS=5000,  # Server selection timeout
            )
            self.db = self.client[database_name]
            
            # Test connection
            self.client.admin.command('ping')
            logger.info(f"Connected to MongoDB: {database_name}")
            
        except PyMongoError as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
    
    def _get_collection(self, collection_name: str) -> Collection:
        """
        Get a MongoDB collection.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            MongoDB collection
        """
        return self.db[collection_name]
    
    def find_one(
        self, collection_name: str, query: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Find a single document in a collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            
        Returns:
            Document or None if not found
        """
        try:
            collection = self._get_collection(collection_name)
            return collection.find_one(query)
        except PyMongoError as e:
            logger.error(f"MongoDB error in find_one: {str(e)}")
            return None
    
    def find_many(
        self,
        collection_name: str,
        query: Dict[str, Any],
        sort: Optional[List[tuple]] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find multiple documents in a collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            sort: Optional sort specification [(field, direction), ...]
            limit: Optional limit on number of results
            skip: Optional number of documents to skip
            
        Returns:
            List of documents
        """
        try:
            collection = self._get_collection(collection_name)
            cursor = collection.find(query)
            
            if sort:
                cursor = cursor.sort(sort)
            
            if skip:
                cursor = cursor.skip(skip)
            
            if limit:
                cursor = cursor.limit(limit)
            
            return list(cursor)
        except PyMongoError as e:
            logger.error(f"MongoDB error in find_many: {str(e)}")
            return []
    
    def insert_one(
        self, collection_name: str, document: Dict[str, Any]
    ) -> Optional[str]:
        """
        Insert a single document into a collection.
        
        Args:
            collection_name: Name of the collection
            document: Document to insert
            
        Returns:
            Inserted document ID or None if failed
        """
        try:
            collection = self._get_collection(collection_name)
            result = collection.insert_one(document)
            return str(result.inserted_id)
        except PyMongoError as e:
            logger.error(f"MongoDB error in insert_one: {str(e)}")
            return None
    
    def insert_many(
        self, collection_name: str, documents: List[Dict[str, Any]]
    ) -> int:
        """
        Insert multiple documents into a collection.
        
        Args:
            collection_name: Name of the collection
            documents: List of documents to insert
            
        Returns:
            Number of documents inserted
        """
        if not documents:
            return 0
        
        try:
            collection = self._get_collection(collection_name)
            result = collection.insert_many(documents)
            return len(result.inserted_ids)
        except PyMongoError as e:
            logger.error(f"MongoDB error in insert_many: {str(e)}")
            return 0
    
    def update_one(
        self,
        collection_name: str,
        query: Dict[str, Any],
        update: Dict[str, Any],
        upsert: bool = False,
    ) -> bool:
        """
        Update a single document in a collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            update: Update operations
            upsert: Whether to insert if not exists
            
        Returns:
            True if successful, False otherwise
        """
        try:
            collection = self._get_collection(collection_name)
            result = collection.update_one(query, update, upsert=upsert)
            return result.modified_count > 0 or (upsert and result.upserted_id is not None)
        except PyMongoError as e:
            logger.error(f"MongoDB error in update_one: {str(e)}")
            return False
    
    def delete_one(self, collection_name: str, query: Dict[str, Any]) -> bool:
        """
        Delete a single document from a collection.
        
        Args:
            collection_name: Name of the collection
            query: Query filter
            
        Returns:
            True if document was deleted, False otherwise
        """
        try:
            collection = self._get_collection(collection_name)
            result = collection.delete_one(query)
            return result.deleted_count > 0
        except PyMongoError as e:
            logger.error(f"MongoDB error in delete_one: {str(e)}")
            return False
    
    def create_index(
        self,
        collection_name: str,
        keys: List[tuple],
        unique: bool = False,
        sparse: bool = False,
    ) -> str:
        """
        Create an index on a collection.
        
        Args:
            collection_name: Name of the collection
            keys: List of (field, direction) tuples
            unique: Whether the index should enforce uniqueness
            sparse: Whether the index should be sparse
            
        Returns:
            Name of the created index
        """
        try:
            collection = self._get_collection(collection_name)
            return collection.create_index(
                keys, unique=unique, sparse=sparse
            )
        except PyMongoError as e:
            logger.error(f"MongoDB error in create_index: {str(e)}")
            raise

