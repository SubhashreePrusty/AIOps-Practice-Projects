import os
import json
import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB
dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "BirthdaysTable")
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Lambda to delete a specific birthday record by name.
    Expected payload:
    {
        "name": "Alice"
    }
    """
    try:
        # Handle both API Gateway and manual test payloads
        if isinstance(event, str):
            event = json.loads(event)
        elif "body" in event:
            body = event["body"]
            if isinstance(body, str):
                body = json.loads(body)
            name = body.get("name")
            birthday = body.get("birthday")  # ✅ new line
        else:
            name = event.get("name")
            birthday = event.get("birthday")

        if not name or not birthday:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'name' or 'birthday' in request"})
            }


        # ✅ Reserved keyword fix using ExpressionAttributeNames
        response = table.delete_item(
            Key={
                "name": name,
                "birthday": birthday
            },
            ConditionExpression="attribute_exists(#n)",
            ExpressionAttributeNames={"#n": "name"}
        )


        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": f"Deleted birthday for {name} successfully!"
            })
        }

    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return {
                "statusCode": 404,
                "body": json.dumps({"error": f"No record found for name '{name}'"})
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }