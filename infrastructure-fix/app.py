#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infrastructure_fix.infrastructure_fix_stack import InfrastructureFixStack


app = cdk.App()
InfrastructureFixStack(app, "InfrastructureFixStack",
    # Issue: Using environment-agnostic deployment
    # For this challenge, we've deliberately left this environment-agnostic
    # which might contribute to the issues.
    
    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.
    # env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    
    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to.
    # env=cdk.Environment(account='123456789012', region='us-east-1'),
    
    description="Infrastructure with DynamoDB and Lambda connection issues to troubleshoot",
)

app.synth()
