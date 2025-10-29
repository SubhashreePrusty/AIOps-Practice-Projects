# Lambda entry point (main)

import json
from utils import response
from db_operations import add_expense, get_expenses, get_monthly_summary, update_expense, delete_expense

def lambda_handler(event, context):
    print("Event received:", event)  # Debug log

    # Handle both REST API and HTTP API event structures
    http_method = (
        event.get("httpMethod") or
        event.get("requestContext", {}).get("http", {}).get("method")
    )
    path = (
        event.get("path") or
        event.get("rawPath") or
        event.get("resource") or
        ""
    )
    params = event.get("queryStringParameters") or {}

    # Parse body safely
    body = {}
    if event.get("body"):
        try:
            body = json.loads(event["body"])
        except Exception:
            body = event["body"]
    print("HTTP method:", http_method, "Path:", path)

    try:
        # ------------------ POST /expenses ------------------
        if http_method == "POST" and path.endswith("/expenses"):
            date = body["date"]
            category = body["category"]
            amount = body["amount"]
            note = body.get("note", "")
            result = add_expense(date, category, amount, note)
            return response(200, result)

        # ------------------ GET /summary ------------------
        elif http_method == "GET" and "/summary" in path:
            month = params.get("month")
            if not month:
                return response(400, {"error": "Please provide month=YYYY-MM in query params"})
            summary = get_monthly_summary(month)
            return response(200, summary)

        # ------------------ GET /expenses ------------------
        elif http_method == "GET" and path.endswith("/expenses"):
            month = params.get("month")
            category = params.get("category")
            items = get_expenses(month, category)
            return response(200, items)
        
        # ------------------ PUT /expenses ------------------
        elif http_method.upper() == "PUT" and "expenses" in path:
            print("PUT body received:", body)  # <— add this
            month_category = body.get("month_category")
            date_id = body.get("date_id")
            new_category = body.get("category")
            new_amount = body.get("amount")
            new_note = body.get("note", "")

            print(f"Updating item {month_category} - {date_id}")

            if not (month_category and date_id):
                return response(400, {"error": "Missing required keys for update"})

            result = update_expense(month_category, date_id, new_category, new_amount, new_note)
            print("Update result:", result)
            return response(200, result)


        # ------------------ DELETE /expenses ------------------
        elif http_method == "DELETE" and "/expenses" in path:
            month_category = body.get("month_category") or params.get("month_category")
            date_id = body.get("date_id") or params.get("date_id")

            if not (month_category and date_id):
                return response(400, {"error": "Missing required keys for delete"})

            result = delete_expense(month_category, date_id)
            return response(200, result)

        # ------------------ Unsupported ------------------
        else:
            return response(400, {"error": "Unsupported method or path"})
        

    except Exception as e:
        print(f"❌ Error: {e}")
        return response(500, {"error": str(e)})
