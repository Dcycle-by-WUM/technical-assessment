#!/usr/bin/env python3
import os
import aws_cdk as cdk
from dotenv import load_dotenv

from infrastructure.customer_data_stack import CustomerDataStack
from infrastructure.monitoring_stack import MonitoringStack

# Load environment variables from .env file if it exists
load_dotenv()

# Get environment from command-line arguments or use default
app = cdk.App()

# Extract environment name from context or use default
env_name = app.node.try_get_context("env") or "dev"
print(f"Deploying to environment: {env_name}")

# Hardcoded account and region - should be environment-specific
# Security concern: Hardcoded credentials and region
account = os.environ.get("CDK_DEFAULT_ACCOUNT", "123456789012")
region = os.environ.get("CDK_DEFAULT_REGION", "us-east-1")

# Environment-specific configuration
env_config = {
    "dev": {
        "instance_type": "t3.micro",
        "min_capacity": 1,
        "max_capacity": 2,
        "environment_name": "development",
    },
    "staging": {
        "instance_type": "t3.small",
        "min_capacity": 2,
        "max_capacity": 4,
        "environment_name": "staging",
    },
    "prod": {
        "instance_type": "t3.medium",
        "min_capacity": 3,
        "max_capacity": 10,
        "environment_name": "production",
    }
}

# Check if the environment is valid
if env_name not in env_config:
    raise ValueError(f"Invalid environment: {env_name}. Must be one of: {', '.join(env_config.keys())}")

config = env_config[env_name]

# Define environment
env = cdk.Environment(account=account, region=region)

# Create stacks
customer_data_stack = CustomerDataStack(
    app, 
    f"CustomerDataStack-{env_name}",
    env=env,
    config=config,
    env_name=env_name,
    description=f"Customer data platform infrastructure for {config['environment_name']} environment"
)

monitoring_stack = MonitoringStack(
    app, 
    f"MonitoringStack-{env_name}",
    env=env,
    config=config,
    env_name=env_name,
    customer_data_stack=customer_data_stack,
    description=f"Monitoring infrastructure for {config['environment_name']} environment"
)

# Tag all resources
for key, value in {
    "Environment": env_name,
    "Application": "CustomerDataPlatform",
    "Owner": "DataTeam",
    # Missing cost allocation tags
}.items():
    cdk.Tags.of(app).add(key, value)

app.synth()

