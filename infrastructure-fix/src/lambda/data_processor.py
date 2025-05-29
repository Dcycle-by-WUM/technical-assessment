import os
import json
import boto3
import logging
import csv
import io
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

# Get environment variables
table_name = os.environ['TABLE_NAME']
export_bucket = os.environ['EXPORT_BUCKET']
environment = os.environ['ENVIRONMENT']

# Initialize DynamoDB table
table = dynamodb.Table(table_name)

def handler(event, context):
    logger.info(f"Processing data for environment: {environment}")
    logger.info(f"Event: {json.dumps(event)}")
    
    try:
        # Get all customers from DynamoDB
        customers = get_all_customers()
        
        # Export customers to S3
        export_customers_to_s3(customers)
        
        # Process customer data (e.g., analytics, aggregations)
        process_customer_data(customers)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully processed {len(customers)} customers',
                'timestamp': datetime.utcnow().isoformat()
            })
        }
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise e

def get_all_customers():
    # Cost concern: Scanning entire table
    # Performance concern: No pagination for large datasets
    logger.info(f"Retrieving all customers from table: {table_name}")
    
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
    
    logger.info(f"Retrieved {len(customers)} customers")
    return customers

def export_customers_to_s3(customers):
    # Security concern: No encryption for S3 objects
    # Data governance concern: No versioning for exports
    if not customers:
        logger.info("No customers to export")
        return
    
    logger.info(f"Exporting {len(customers)} customers to S3 bucket: {export_bucket}")
    
    # Create CSV in memory
    csv_buffer = io.StringIO()
    csv_writer = csv.writer(csv_buffer)
    
    # Write headers
    csv_writer.writerow(['id', 'firstName', 'lastName', 'email', 'createdAt', 'updatedAt'])
    
    # Write customer data
    for customer in customers:
        csv_writer.writerow([
            customer['id'],
            customer['firstName'],
            customer['lastName'],
            customer['email'],
            customer['createdAt'],
            customer['updatedAt']
        ])
    
    # Generate filename with timestamp
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    filename = f"customer-export-{environment}-{timestamp}.csv"
    
    # Upload to S3
    s3.put_object(
        Bucket=export_bucket,
        Key=filename,
        Body=csv_buffer.getvalue(),
        ContentType='text/csv'
    )
    
    logger.info(f"Successfully exported customers to S3: {filename}")

def process_customer_data(customers):
    # Simulate data processing tasks
    logger.info("Processing customer data for analytics")
    
    # Count customers by creation month
    customers_by_month = {}
    for customer in customers:
        try:
            created_date = datetime.fromisoformat(customer['createdAt'])
            month_key = created_date.strftime('%Y-%m')
            
            if month_key in customers_by_month:
                customers_by_month[month_key] += 1
            else:
                customers_by_month[month_key] = 1
        except (ValueError, TypeError):
            logger.warning(f"Invalid date format for customer: {customer['id']}")
    
    logger.info(f"Customers by month: {json.dumps(customers_by_month)}")
    
    # Simulate writing aggregated data back to DynamoDB
    # Performance concern: No batch write for efficiency
    timestamp = datetime.utcnow().isoformat()
    
    for month, count in customers_by_month.items():
        table.put_item(
            Item={
                'PK': f'ANALYTICS#MONTHLY',
                'SK': f'CUSTOMER_COUNT#{month}',
                'count': count,
                'updatedAt': timestamp
            }
        )
    
    logger.info("Successfully processed and stored customer analytics")

