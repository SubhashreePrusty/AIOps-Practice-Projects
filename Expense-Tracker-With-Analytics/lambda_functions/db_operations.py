# DynamoDB CRUD operations

import os
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.getenv("DYNAMODB_TABLE", "PersonalExpenses")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def add_expense(item: dict):
    """Insert a new expense item into DynamoDB"""
    if isinstance(item.get("amount"), float):
        item["amount"] = Decimal(str(item["amount"]))
    table.put_item(Item=item)
    return {"status": "success", "message": "Expense added successfully"}


def get_all_expenses():
    """Return all expense items"""
    resp = table.scan()
    items = resp.get("Items", [])
    # Convert Decimal → float
    for item in items:
        if "amount" in item:
            item["amount"] = float(item["amount"])
    return items


def get_category_summary():
    """Aggregate total spent per category"""
    items = get_all_expenses()
    summary = {}
    for i in items:
        category = i.get("category", "Unknown")
        summary[category] = summary.get(category, 0) + i.get("amount", 0)
    result = [{"category": k, "total_amount": v} for k, v in summary.items()]
    return result
