from aws_cdk import (
    Stack,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as actions,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_iam as iam,
    aws_chatbot as chatbot,
    Duration,
)
from constructs import Construct

class MonitoringStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, env_name: str, config: dict, customer_data_stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Determine if this is a production environment
        is_production = env_name == "prod"
        
        # Create SNS topic for alerts
        # Security concern: No encryption for SNS topic
        # Operational concern: No subscription filter policy
        alert_topic = sns.Topic(
            self, 
            f"AlertTopic-{env_name}",
            display_name=f"Customer Data Platform Alerts ({env_name})",
            topic_name=f"customer-data-platform-alerts-{env_name}",
        )
        
        # Add email subscription
        # Security concern: Email hardcoded, different for each environment
        # Operational concern: No confirmation for subscription
        if env_name == "prod":
            alert_topic.add_subscription(
                subscriptions.EmailSubscription("prod-alerts@example.com")
            )
        elif env_name == "staging":
            alert_topic.add_subscription(
                subscriptions.EmailSubscription("staging-alerts@example.com")
            )
        else:
            alert_topic.add_subscription(
                subscriptions.EmailSubscription("dev-alerts@example.com")
            )
        
        # Add SMS subscription for production only
        # Cost concern: SMS can be expensive
        if is_production:
            alert_topic.add_subscription(
                subscriptions.SmsSubscription("+1234567890")
            )
        
        # Create dashboard
        # Operational concern: Different dashboards for different environments
        dashboard = cloudwatch.Dashboard(
            self, 
            f"CustomerDataDashboard-{env_name}",
            dashboard_name=f"CustomerDataPlatform-{env_name}",
        )
        
        # Add widgets to dashboard
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title=f"Customer API Lambda Invocations ({env_name})",
                left=[
                    customer_data_stack.customer_api_lambda.metric_invocations(),
                ],
            ),
            cloudwatch.GraphWidget(
                title=f"Customer API Lambda Errors ({env_name})",
                left=[
                    customer_data_stack.customer_api_lambda.metric_errors(),
                ],
            ),
            cloudwatch.GraphWidget(
                title=f"Customer API Lambda Duration ({env_name})",
                left=[
                    customer_data_stack.customer_api_lambda.metric_duration(),
                ],
            ),
        )
        
        # Add DynamoDB metrics
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title=f"DynamoDB Read Capacity ({env_name})",
                left=[
                    customer_data_stack.customer_table.metric_consumed_read_capacity_units(),
                ],
            ),
            cloudwatch.GraphWidget(
                title=f"DynamoDB Write Capacity ({env_name})",
                left=[
                    customer_data_stack.customer_table.metric_consumed_write_capacity_units(),
                ],
            ),
        )
        
        # Create alarms
        # Operational concern: Different thresholds for different environments
        # Operational concern: No composite alarms
        lambda_error_alarm = cloudwatch.Alarm(
            self, 
            f"LambdaErrorAlarm-{env_name}",
            metric=customer_data_stack.customer_api_lambda.metric_errors(),
            threshold=5 if is_production else 10,
            evaluation_periods=3,
            datapoints_to_alarm=2,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            alarm_description=f"Alert when Lambda errors exceed threshold in {env_name}",
            alarm_name=f"CustomerApiLambdaErrors-{env_name}",
        )
        
        lambda_duration_alarm = cloudwatch.Alarm(
            self, 
            f"LambdaDurationAlarm-{env_name}",
            metric=customer_data_stack.customer_api_lambda.metric_duration(),
            threshold=5000 if is_production else 10000,  # 5 seconds for prod, 10 for others
            evaluation_periods=3,
            datapoints_to_alarm=2,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            alarm_description=f"Alert when Lambda duration exceeds threshold in {env_name}",
            alarm_name=f"CustomerApiLambdaDuration-{env_name}",
        )
        
        # Add alarm actions
        lambda_error_alarm.add_alarm_action(actions.SnsAction(alert_topic))
        lambda_duration_alarm.add_alarm_action(actions.SnsAction(alert_topic))
        
        # Set up ChatBot integration for Slack (production only)
        # Operational concern: Only available in production
        # Security concern: Hardcoded workspace ID and channel
        if is_production:
            slack_channel = chatbot.SlackChannelConfiguration(
                self, 
                "AlertSlackChannel",
                slack_channel_configuration_name="customer-data-platform-alerts",
                slack_workspace_id="T0123456789",
                slack_channel_id="C0123456789",
                notification_topics=[alert_topic],
            )
        
        # Export properties for other stacks
        self.alert_topic = alert_topic
        self.dashboard = dashboard

