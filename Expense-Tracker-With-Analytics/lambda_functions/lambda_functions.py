# Lambda entry point (main)

import json
from utils import response
from db_operations import add_expense, get_expenses, get_monthly_summary

def lambda_handler(event, context):
    http_method = event.get("httpMethod")
    path = event.get("path", "")
    params = event.get("queryStringParameters") or {}

    try:
        # ------------------ POST /expenses ------------------
        if http_method == "POST" and path.endswith("/expenses"):
            body = json.loads(event["body"])
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

        # ------------------ Unsupported ------------------
        else:
            return response(400, {"error": "Unsupported method or path"})

    except Exception as e:
        print(f"❌ Error: {e}")
        return response(500, {"error": str(e)})




 








    
    
      
      