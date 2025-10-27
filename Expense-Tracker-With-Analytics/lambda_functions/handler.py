# Lambda entry point (main)

import json
import uuid
from utils import response, get_current_timestamp
from db_operations import add_expense, get_all_expenses, get_category_summary


def lambda_handler(event, context):
    """Lambda entry point triggered by API Gateway"""
    print("Received event:", json.dumps(event))

    http_method = event.get("httpMethod", "")
    path = event.get("path", "")

    # Handle preflight (CORS)
    if http_method == "OPTIONS":
        return response(200, {"message": "CORS preflight OK"})

    try:
        # 1️⃣ ADD NEW EXPENSE (POST /expenses)
        if http_method == "POST" and path.endswith("/expenses"):
            body = json.loads(event.get("body", "{}"))
            new_item = {
                "expense_id": str(uuid.uuid4()),
                "date": body["date"],
                "category": body["category"],
                "amount": float(body["amount"]),
                "note": body.get("note", ""),
                "created_at": get_current_timestamp()
            }
            result = add_expense(new_item)
            return response(200, result)

        # 2️⃣ GET ALL EXPENSES (GET /expenses)
        elif http_method == "GET" and path.endswith("/expenses"):
            items = get_all_expenses()
            return response(200, items)

        # 3️⃣ CATEGORY SUMMARY (GET /summary)
        elif http_method == "GET" and path.endswith("/summary"):
            summary = get_category_summary()
            return response(200, summary)

        else:
            return response(400, {"status": "error", "message": "Invalid route or method"})

    except Exception as e:
        print("Error:", str(e))
        return response(500, {"status": "error", "message": str(e)})
