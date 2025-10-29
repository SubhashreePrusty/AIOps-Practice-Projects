
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

def update_expense(month_category, date_id, new_category, new_amount, new_note):
    """
    Update an existing expense. If new_category would change the partition key
    (month_category), perform copy+put+delete to move item to new partition.
    """
    try:
        # 1) Get the existing item (safe-read)
        resp = table.get_item(Key={"month_category": month_category, "date_id": date_id})
        item = resp.get("Item")
        if not item:
            return {"status": "error", "message": "Item not found."}

        # Determine the new month_category based on item's date (and new_category)
        date_str = item.get("date", "")
        if not date_str:
            return {"status": "error", "message": "Existing item missing date."}
        new_month_category = f"{date_str[:7]}#{new_category}"

        # If partition (month_category) unchanged, just update attributes
        if new_month_category == month_category:
            response = table.update_item(
                Key={"month_category": month_category, "date_id": date_id},
                UpdateExpression="SET category = :c, amount = :a, note = :n",
                ExpressionAttributeValues={
                    ":c": new_category,
                    ":a": Decimal(str(new_amount)),
                    ":n": new_note
                },
                ReturnValues="UPDATED_NEW"
            )
            return {"status": "success", "message": "Expense updated!", "updated": response.get("Attributes")}

        # Else: need to create the new item then delete the old item
        new_item = item.copy()
        new_item["month_category"] = new_month_category
        new_item["category"] = new_category
        new_item["amount"] = Decimal(str(new_amount))
        new_item["note"] = new_note

        # Put new item (this overwrites if one exists with same keys)
        table.put_item(Item=new_item)

        # Delete old item
        table.delete_item(Key={"month_category": month_category, "date_id": date_id})

        return {"status": "success", "message": "Expense moved & updated!"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_expense(month_category, date_id): 
    """Delete an expense""" 
    try: 
        table.delete_item(Key={"month_category": month_category, "date_id": date_id}) 
        return {"status": "success", "message": "Expense deleted!"} 
    except Exception as e: 
        return {"status": "error", "message": str(e)}
