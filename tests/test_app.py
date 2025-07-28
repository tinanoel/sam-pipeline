import json
import app
from moto import mock_sns
import boto3
import os

@mock_sns
def test_lambda_handler():
    # Create a fake SNS topic
    sns = boto3.client("sns", region_name="ap-south-1")
    topic_arn = sns.create_topic(Name="sns-demo")["TopicArn"]
    os.environ["SNS_TOPIC_ARN"] = topic_arn

    # Mock DynamoDB Stream INSERT event
    event = {
        "Records": [
            {
                "eventName": "INSERT",
                "dynamodb": {
                    "NewImage": {
                        "OrderId": {"S": "ORDER123"},
                        "Amount": {"N": "1000"},
                        "CustomerEmail": {"S": "test@example.com"}
                    }
                }
            }
        ]
    }

    # Call Lambda
    result = app.lambda_handler(event, None)
    assert result is None  # No return, but should not fail
