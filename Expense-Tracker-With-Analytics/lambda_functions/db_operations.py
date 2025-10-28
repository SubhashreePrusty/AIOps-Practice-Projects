
# DynamoDB CRUD operations

# DynamoDB CRUD operations
import os
import boto3
import uuid
from decimal import Decimal
from boto3.dynamodb.conditions import Key
from collections import defaultdict

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
    """Return category-wise total expenses for the given month"""
    response = table.scan()
    items = response.get("Items", [])

    category_totals = defaultdict(Decimal)

    # Aggregate totals for items belonging to this month
    for item in items:
        if item.get("date", "").startswith(month):
            category = item.get("category", "Unknown")
            amount = Decimal(str(item.get("amount", 0)))
            category_totals[category] += amount

    # Convert to simple JSON-serializable list
    summary = [{"category": cat, "total": float(total)} for cat, total in category_totals.items()]
    return summary


