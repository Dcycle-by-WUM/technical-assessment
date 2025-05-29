import os
import json
import boto3
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
# Issue #6: Not properly handling regional configuration
dynamodb = boto3.resource('dynamodb')  # Missing region parameter

# Get table name from environment variable
# Issue #7: Not handling missing environment variables
table_name = os.environ['TABLE_NAME']  # Will crash if env var is missing

# Initialize table resource
# Issue #8: Not handling table initialization errors
table = dynamodb.Table(table_name)

def handler(event, context):
    """
    Lambda handler to process user data and store in DynamoDB.
    
    Args:
        event (dict): Lambda event data
        context (LambdaContext): Lambda context
        
    Returns:
        dict: Response with status and message
    """
    logger.info("Processing user data event: %s", json.dumps(event))
    
    try:
        # Extract user data from event
        user_data = event.get('user', {})
        
        if not user_data or not user_data.get('userId'):
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'Missing required user data'
                })
            }
        
        # Issue #9: Not handling DynamoDB item size limits
        # Prepare item for DynamoDB
        timestamp = int(datetime.now().timestamp() * 1000)
        
        item = {
            'userId': user_data['userId'],
            'timestamp': timestamp,
            'data': user_data
        }
        
        # Issue #10: Not implementing proper error handling
        # Put item in DynamoDB table
        response = table.put_item(Item=item)
        
        logger.info("Successfully processed user data: %s", user_data['userId'])
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'User data processed successfully',
                'userId': user_data['userId'],
                'timestamp': timestamp
            })
        }
        
    except Exception as e:
        # Issue #11: Poor error handling - not enough detail
        logger.error("Error processing user data: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error processing user data'
            })
        }

def get_user_data(user_id):
    """
    Retrieve user data from DynamoDB.
    
    Args:
        user_id (str): The user ID to retrieve
        
    Returns:
        dict: User data or None if not found
    """
    try:
        # Issue #12: Inefficient query - should use query instead of scan
        # Also incorrect use of FilterExpression instead of KeyConditionExpression
        response = table.scan(
            FilterExpression='userId = :userId',
            ExpressionAttributeValues={
                ':userId': user_id
            }
        )
        
        items = response.get('Items', [])
        
        if not items:
            logger.info("No data found for user: %s", user_id)
            return None
            
        return items[0]
        
    except Exception as e:
        logger.error("Error retrieving user data: %s", str(e))
        return None

