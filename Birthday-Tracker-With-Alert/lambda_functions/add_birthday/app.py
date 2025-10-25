import os
import json
import uuid
from datetime import datetime
import boto3
from dateutil.parser import parse as parse_date

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "BirthdaysTable")
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)

        name = body.get("name")
        dob = body.get("birthday")

        if not name or not dob:
            return {"statusCode": 400, "body": json.dumps({"message":"name and birthday required"})}

        # Validate date format
        dt = parse_date(dob).date()

        # Prepare item
        item = {
            "id": str(uuid.uuid4()),
            "name": name,
            "birthday": dt.isoformat(),
            "created_at": datetime.utcnow().isoformat() + "Z",
        }

        # Put item into DynamoDB
        table.put_item(Item=item)

        return {"statusCode": 201, "body": json.dumps({"message":"created","item":item})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": "error", "error": str(e)})}
