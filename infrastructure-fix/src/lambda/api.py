import os
import json
import boto3
import logging
from datetime import datetime
import uuid

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

# Security concern: No input validation
# Security concern: No proper error handling

def handler(event, context):
    logger.info(f"Event: {json.dumps(event)}")
    
    # Extract HTTP method and path parameters
    http_method = event['httpMethod']
    path = event['path']
    
    # Initialize response
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # Security concern: CORS allows all origins
        }
    }
    
    try:
        # Route request based on HTTP method and path
        if http_method == 'GET' and path == '/customers':
            # List all customers
            response['body'] = json.dumps(get_all_customers())
        elif http_method == 'GET' and path.startswith('/customers/'):
            # Get specific customer
            customer_id = event['pathParameters']['customerId']
            response['body'] = json.dumps(get_customer(customer_id))
        elif http_method == 'POST' and path == '/customers':
            # Create new customer
            body = json.loads(event['body'])
            response['body'] = json.dumps(create_customer(body))
        elif http_method == 'PUT' and path.startswith('/customers/'):
            # Update existing customer
            customer_id = event['pathParameters']['customerId']
            body = json.loads(event['body'])
            response['body'] = json.dumps(update_customer(customer_id, body))
        elif http_method == 'DELETE' and path.startswith('/customers/'):
            # Delete customer
            customer_id = event['pathParameters']['customerId']
            response['body'] = json.dumps(delete_customer(customer_id))
        else:
            # Handle unsupported routes
            response['statusCode'] = 404
            response['body'] = json.dumps({'error': 'Not Found'})
    except Exception as e:
        # Security concern: Exposing error details to clients
        logger.error(f"Error processing request: {str(e)}")
        response['statusCode'] = 500
        response['body'] = json.dumps({'error': str(e)})
    
    return response

def get_all_customers():
    # Performance concern: No pagination
    # Cost concern: Scanning entire table
    result = table.scan()
    
    customers = []
    for item in result.get('Items', []):
        if item.get('SK', '').startswith('PROFILE#'):
            customers.append({
                'id': item['PK'].replace('CUSTOMER#', ''),
                'firstName': item.get('firstName', ''),
                'lastName': item.get('lastName', ''),
                'email': item.get('email', ''),
                'createdAt': item.get('createdAt', ''),
                'updatedAt': item.get('updatedAt', '')
            })
    
    return {'customers': customers}

def get_customer(customer_id):
    # Security concern: No validation of customer_id
    result = table.get_item(
        Key={
            'PK': f'CUSTOMER#{customer_id}',
            'SK': 'PROFILE#V1'
        }
    )
    
    item = result.get('Item')
    if not item:
        raise Exception(f"Customer not found: {customer_id}")
    
    return {
        'id': item['PK'].replace('CUSTOMER#', ''),
        'firstName': item.get('firstName', ''),
        'lastName': item.get('lastName', ''),
        'email': item.get('email', ''),
        'createdAt': item.get('createdAt', ''),
        'updatedAt': item.get('updatedAt', '')
    }

def create_customer(customer_data):
    # Security concern: No validation of customer_data
    # Security concern: No protection against duplicate emails
    
    # Generate customer ID
    customer_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    
    # Prepare item for DynamoDB
    item = {
        'PK': f'CUSTOMER#{customer_id}',
        'SK': 'PROFILE#V1',
        'firstName': customer_data.get('firstName', ''),
        'lastName': customer_data.get('lastName', ''),
        'email': customer_data.get('email', ''),
        'createdAt': timestamp,
        'updatedAt': timestamp
    }
    
    # Write to DynamoDB
    table.put_item(Item=item)
    
    return {
        'id': customer_id,
        'firstName': item['firstName'],
        'lastName': item['lastName'],
        'email': item['email'],
        'createdAt': item['createdAt'],
        'updatedAt': item['updatedAt']
    }

def update_customer(customer_id, customer_data):
    # Security concern: No validation of customer_id or customer_data
    # Check if customer exists
    result = table.get_item(
        Key={
            'PK': f'CUSTOMER#{customer_id}',
            'SK': 'PROFILE#V1'
        }
    )
    
    item = result.get('Item')
    if not item:
        raise Exception(f"Customer not found: {customer_id}")
    
    # Update timestamp
    timestamp = datetime.utcnow().isoformat()
    
    # Prepare update expression
    update_expression = "SET updatedAt = :updatedAt"
    expression_attribute_values = {
        ':updatedAt': timestamp
    }
    
    # Add customer data fields to update expression
    for key, value in customer_data.items():
        if key not in ['id', 'createdAt', 'updatedAt']:
            update_expression += f", {key} = :{key}"
            expression_attribute_values[f':{key}'] = value
    
    # Update item in DynamoDB
    result = table.update_item(
        Key={
            'PK': f'CUSTOMER#{customer_id}',
            'SK': 'PROFILE#V1'
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='ALL_NEW'
    )
    
    updated_item = result.get('Attributes', {})
    
    return {
        'id': customer_id,
        'firstName': updated_item.get('firstName', ''),
        'lastName': updated_item.get('lastName', ''),
        'email': updated_item.get('email', ''),
        'createdAt': updated_item.get('createdAt', ''),
        'updatedAt': updated_item.get('updatedAt', '')
    }

def delete_customer(customer_id):
    # Security concern: No validation of customer_id
    # Check if customer exists
    result = table.get_item(
        Key={
            'PK': f'CUSTOMER#{customer_id}',
            'SK': 'PROFILE#V1'
        }
    )
    
    item = result.get('Item')
    if not item:
        raise Exception(f"Customer not found: {customer_id}")
    
    # Delete item from DynamoDB
    table.delete_item(
        Key={
            'PK': f'CUSTOMER#{customer_id}',
            'SK': 'PROFILE#V1'
        }
    )
    
    return {
        'id': customer_id,
        'deleted': True
    }

