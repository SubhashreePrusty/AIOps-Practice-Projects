import json
import boto3
import os

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "BirthdaysTable")
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        # Scan all items in the table
        response = table.scan()
        items = response.get('Items', [])

        return {
            "statusCode": 200,
            "body": json.dumps({"items": items}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }
