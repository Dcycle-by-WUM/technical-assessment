from aws_cdk import (
    Duration,
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_iam as iam,
)
from constructs import Construct

class InfrastructureFixStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a DynamoDB table
        user_table = dynamodb.Table(
            self, "UserTable",
            partition_key=dynamodb.Attribute(
                name="userId",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp",
                type=dynamodb.AttributeType.NUMBER
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY  # For demo purposes only
        )
        
        # Create Lambda function
        user_processor = lambda_.Function(
            self, "UserProcessor",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("lambda"),
            handler="user_processor.handler",
            environment={
                # Issue #1: Wrong table name format - should be using full ARN or just the name
                "TABLE_NAME": f"UserTable-{user_table.table_name}",  # Incorrect format
                # Issue #2: Missing region environment variable
                # "AWS_REGION": self.region,
            },
            timeout=Duration.seconds(30),
        )
        
        # Issue #3: Incomplete IAM permissions - missing proper DynamoDB permissions
        # Using a policy that only grants partial permissions
        user_processor.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "dynamodb:GetItem",  # Missing required permissions: PutItem, Query, etc.
                ],
                # Issue #4: Incorrect resource specification - using wrong ARN format
                resources=[f"arn:aws:dynamodb:{self.region}:{self.account}:table/{user_table.table_name}*"]
            )
        )
        
        # Issue #5: Missing resource policy or incorrect cross-account permissions
        # if needed for this scenario
        
        # Output the function name and table name for testing
        CfnOutput(self, "UserProcessorFunction", value=user_processor.function_name)
        CfnOutput(self, "UserTableName", value=user_table.table_name)
