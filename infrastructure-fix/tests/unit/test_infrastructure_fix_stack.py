import aws_cdk as core
import aws_cdk.assertions as assertions

from infrastructure_fix.infrastructure_fix_stack import InfrastructureFixStack

# example tests. To run these tests, uncomment this file along with the example
# resource in infrastructure_fix/infrastructure_fix_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = InfrastructureFixStack(app, "infrastructure-fix")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
