# Lambda Functions

This directory contains the Lambda functions that are deployed as part of the infrastructure.

## Structure

- `user_processor.py` - Main Lambda handler that processes user data and interacts with DynamoDB
- `__init__.py` - Package initialization file

## User Processor Lambda

The User Processor Lambda function is designed to:

1. Receive user data in an event
2. Process and validate the data
3. Store the data in a DynamoDB table
4. Retrieve user data when requested

## Testing Locally

You can test the Lambda function locally by setting up a mock environment:

```python
import json
from user_processor import handler

event = {
    'user': {
        'userId': 'user123',
        'name': 'Test User',
        'email': 'test@example.com'
    }
}

context = {}

response = handler(event, context)
print(json.dumps(response, indent=2))
```

## Common Errors

When the Lambda function is deployed, you might encounter these errors:

- `ResourceNotFoundException`: The DynamoDB table cannot be found
- `AccessDeniedException`: The Lambda doesn't have permissions to access the table
- `ValidationException`: The DynamoDB operation failed validation

These errors are part of the infrastructure challenge and need to be diagnosed and fixed.

