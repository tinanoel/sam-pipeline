import os
import json
import boto3

sns = boto3.client("sns")
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]

def lambda_handler(event, context):
    for record in event["Records"]:
        if record["eventName"] != "INSERT":
            continue

        item = record["dynamodb"]["NewImage"]
        order_id = item["OrderId"]["S"]
        amount   = item.get("Amount", {}).get("N", "0")
        customer = item.get("CustomerEmail", {}).get("S", "unknown")

        message = (
            f"✅ New order placed\n"
            f"Order ID : {order_id}\n"
            f"Customer : {customer}\n"
            f"Amount   : ₹{amount}"
        )

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"Order {order_id} confirmed",
            Message=message
        )

        print(f"Published notification for order {order_id}")