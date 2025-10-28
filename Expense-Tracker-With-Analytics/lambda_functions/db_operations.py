
# DynamoDB CRUD operations

# DynamoDB CRUD operations
import os
import boto3
import uuid
from decimal import Decimal
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table_name = os.environ["DYNAMODB_TABLE"]
table = dynamodb.Table(table_name)

def add_expense(date, category, amount, note=""):
    """Add a new expense item"""
    month_category = f"{date[:7]}#{category}"
    date_id = f"{date}#{str(uuid.uuid4())}"

    item = {
        "month_category": month_category,
        "date_id": date_id,
        "date": date,
        "category": category,
        "amount": Decimal(str(amount)),
        "note": note
    }

    table.put_item(Item=item)
    return {"status": "success", "message": "Expense added!"}


def get_expenses(month=None, category=None):
    """Fetch expenses (all or filtered by month/category)"""
    if month and category:
        month_category = f"{month}#{category}"
        response = table.query(
            KeyConditionExpression=Key("month_category").eq(month_category)
        )
    else:
        response = table.scan()

    return response.get("Items", [])


def get_monthly_summary(month):
    """Fetch category-wise summary for a month"""
    response = table.scan()
    items = response.get("Items", [])

    filtered = [i for i in items if i["month_category"].startswith(month)]

    summary = {}
    for i in filtered:
        cat = i["category"]
        summary[cat] = summary.get(cat, 0) + float(i["amount"])

    return [{"category": k, "amount": v} for k, v in summary.items()]


