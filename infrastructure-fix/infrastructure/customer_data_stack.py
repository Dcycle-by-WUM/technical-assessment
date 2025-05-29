from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as targets,
    aws_s3 as s3,
    aws_kms as kms,
    Duration,
    RemovalPolicy,
)
from constructs import Construct

class CustomerDataStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, env_name: str, config: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Determine if this is a production environment
        is_production = env_name == "prod"
        
        # Define removal policy based on environment
        # Security/operational concern: Non-production environments use DESTROY
        removal_policy = RemovalPolicy.RETAIN if is_production else RemovalPolicy.DESTROY
        
        # Create KMS key for encryption
        # Security concern: Key rotation not enabled, no key policy defined
        encryption_key = kms.Key(
            self, 
            f"CustomerDataKey-{env_name}",
            enable_key_rotation=False,
            removal_policy=removal_policy,
        )
        
        # Create S3 bucket for data exports
        # Security concern: No server-side encryption by default
        # Security concern: No public access block configuration
        # Cost concern: No lifecycle rules defined
        export_bucket = s3.Bucket(
            self, 
            f"CustomerDataExports-{env_name}",
            removal_policy=removal_policy,
            encryption=s3.BucketEncryption.S3_MANAGED,
        )
        
        # Create DynamoDB table - same table for all data types
        # Design concern: Single table for all data types, no separation of concerns
        # Security concern: No encryption with customer managed key
        # Cost concern: No auto scaling configuration
        customer_table = dynamodb.Table(
            self, 
            f"CustomerTable-{env_name}",
            partition_key=dynamodb.Attribute(
                name="PK", 
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="SK", 
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PROVISIONED,
            read_capacity=10,
            write_capacity=5,
            removal_policy=removal_policy,
            point_in_time_recovery=is_production,
            # Stream not enabled for non-production environments
            # Operational concern: Different configuration between environments
            stream=dynamodb.StreamViewType.NEW_AND_OLD_IMAGES if is_production else None,
        )
        
        # Optimization opportunity: No time-to-live configurations
        # Optimization opportunity: No global secondary indexes for common query patterns
        
        # Create Lambda execution role
        # Security concern: Overly permissive role
        lambda_role = iam.Role(
            self, 
            f"CustomerDataLambdaRole-{env_name}",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                # Security concern: Overly permissive policy for DynamoDB
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
                # Security concern: Overly permissive policy for S3
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
            ]
        )
        
        # Create Lambda functions
        # Operational concern: No X-Ray tracing
        # Security concern: Environment variables not encrypted
        # Cost concern: High memory allocation
        # Operational concern: No function versioning
        customer_api_lambda = lambda_.Function(
            self, 
            f"CustomerApiLambda-{env_name}",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="api.handler",
            code=lambda_.Code.from_asset("src/lambda"),
            role=lambda_role,
            environment={
                "ENVIRONMENT": env_name,
                "TABLE_NAME": customer_table.table_name,
                "EXPORT_BUCKET": export_bucket.bucket_name,
                # Security concern: No encryption of environment variables
                "API_KEY": "dev-api-key-12345" if env_name == "dev" else "prod-api-key-67890",
            },
            memory_size=1024,
            timeout=Duration.seconds(30),
            # X-Ray not enabled for all environments
            tracing=lambda_.Tracing.ACTIVE if is_production else lambda_.Tracing.DISABLED,
        )
        
        # Create API Gateway
        # Security concern: No WAF protection
        # Security concern: No API key validation
        # Security concern: CORS configured to allow all origins
        api = apigateway.RestApi(
            self, 
            f"CustomerApi-{env_name}",
            rest_api_name=f"Customer API ({env_name})",
            description=f"API for customer data platform ({env_name})",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=["*"],
                allow_methods=["GET", "POST", "PUT", "DELETE"],
            ),
            deploy_options=apigateway.StageOptions(
                stage_name=env_name,
                # No caching for any environment
                cache_cluster_enabled=False,
                # No throttling configured
                throttling_rate_limit=10000 if is_production else 1000,
                throttling_burst_limit=5000 if is_production else 500,
                # Logging not enabled for non-production
                logging_level=apigateway.MethodLoggingLevel.INFO if is_production else apigateway.MethodLoggingLevel.OFF,
            ),
        )
        
        # Create API resources and methods
        customers_resource = api.root.add_resource("customers")
        customers_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(customer_api_lambda),
        )
        customers_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(customer_api_lambda),
        )
        
        customer_resource = customers_resource.add_resource("{customerId}")
        customer_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(customer_api_lambda),
        )
        customer_resource.add_method(
            "PUT",
            apigateway.LambdaIntegration(customer_api_lambda),
        )
        customer_resource.add_method(
            "DELETE",
            apigateway.LambdaIntegration(customer_api_lambda),
        )
        
        # Create data processing Lambda
        # Operational concern: No X-Ray tracing
        # Security concern: Overly permissive role
        data_processor_lambda = lambda_.Function(
            self, 
            f"DataProcessorLambda-{env_name}",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="data_processor.handler",
            code=lambda_.Code.from_asset("src/lambda"),
            role=lambda_role,
            environment={
                "ENVIRONMENT": env_name,
                "TABLE_NAME": customer_table.table_name,
                "EXPORT_BUCKET": export_bucket.bucket_name,
            },
            memory_size=1024,
            timeout=Duration.seconds(60),
            tracing=lambda_.Tracing.ACTIVE if is_production else lambda_.Tracing.DISABLED,
        )
        
        # Set up scheduled event rule
        # Operational concern: Different schedule for different environments
        # Operational concern: No dead-letter queue for failed executions
        event_rule = events.Rule(
            self, 
            f"DataProcessingRule-{env_name}",
            schedule=events.Schedule.cron(
                minute="0",
                hour="0" if is_production else "*/3",  # Daily in prod, every 3 hours in non-prod
            ),
            targets=[targets.LambdaFunction(data_processor_lambda)],
        )
        
        # Set exports for cross-stack references
        self.customer_table = customer_table
        self.customer_api_lambda = customer_api_lambda
        self.data_processor_lambda = data_processor_lambda
        self.api = api
        self.export_bucket = export_bucket

