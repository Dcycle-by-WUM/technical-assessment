# Infrastructure Connection Fix Challenge

## Overview

This challenge assesses your ability to troubleshoot and fix infrastructure issues - a critical skill for engineering managers who need to support their teams in resolving complex cloud architecture problems. You will debug and fix a connection issue between an AWS Lambda function and a DynamoDB table in a CDK application.

## Challenge Description

You have inherited a CDK application that deploys a serverless architecture consisting of a Lambda function that should read from and write to a DynamoDB table. However, the Lambda function is failing to connect to the DynamoDB table properly.

Your task is to:

1. Identify the root cause of the connection issue
2. Fix the CDK code to resolve the problem
3. Ensure the Lambda function can successfully interact with the DynamoDB table
4. Document your troubleshooting process and the solution implemented

## Problem Details

The architecture includes:
- A DynamoDB table for storing user data
- A Lambda function that processes user data and interacts with the table
- IAM roles and policies that should grant proper permissions
- Environment variables and configurations for connecting components

The Lambda function is currently failing with errors when attempting to access the DynamoDB table. These errors might include permission issues, configuration problems, or other AWS service integration challenges.

## Common Issues to Look For

When troubleshooting AWS infrastructure issues, consider these common problem areas:

1. **IAM permissions** - Are the right permissions granted to the Lambda's execution role?
2. **Resource naming and references** - Are resources properly referenced by ARN, name, or other identifiers?
3. **Environment variables** - Are necessary environment variables set and correctly formatted?
4. **Regional configuration** - Are all resources in the same region, or are cross-region references properly configured?
5. **Resource policies** - Are there resource policies restricting access?
6. **Error handling** - Is the code properly handling errors and providing useful diagnostics?

## Evaluation Criteria

Your solution will be evaluated based on:

1. **Problem identification** - How effectively did you diagnose the root cause?
2. **Solution correctness** - Does your fix resolve the connection issue?
3. **AWS knowledge** - Do you demonstrate understanding of AWS services and their interactions?
4. **CDK expertise** - How well do you utilize CDK constructs and best practices?
5. **Security consciousness** - Is your solution secure and following principle of least privilege?
6. **Documentation** - How clearly do you explain your troubleshooting process and solution?

## Submission Guidelines

1. Fork this repository and implement your fixes
2. Document your troubleshooting steps and findings
3. Explain the changes you made and why they resolve the issue
4. Include any relevant screenshots or logs that helped diagnose the problem
5. Provide instructions on how to deploy and test your fixed solution

## Time Expectation

We expect this challenge to take approximately 60-90 minutes to complete.

## Getting Started

1. Set up your AWS environment using awslogin as specified in the repository guidelines
2. Install the required dependencies
3. Explore the CDK application structure
4. Deploy the application and observe the issue
5. Troubleshoot and fix the connection problem

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Synthesize the CloudFormation template
cdk synth

# Deploy the stack (requires AWS credentials)
cdk deploy
```

## Repository Structure

- `infrastructure_fix/` - CDK application code
- `lambda/` - Lambda function code that interacts with DynamoDB
- `tests/` - Unit tests for the infrastructure

## Known Symptoms

When you deploy and test this infrastructure, you may observe one or more of these errors:

1. "ResourceNotFoundException" when the Lambda tries to access the DynamoDB table
2. "AccessDeniedException" indicating permission issues
3. Timeout errors when the Lambda function executes
4. CloudWatch logs showing connection failures

Your task is to determine which of these issues (or others) are occurring and why, then fix them.


# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
