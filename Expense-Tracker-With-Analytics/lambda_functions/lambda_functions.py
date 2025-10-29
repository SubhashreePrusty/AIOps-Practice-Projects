# Lambda entry point (main)

import json
from utils import response
from db_operations import add_expense, get_expenses, get_monthly_summary, update_expense, delete_expense

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
        
        # ✅ UPDATE EXPENSE (Edit)
        elif http_method == "PUT" and "/expenses" in path:
            month_category = body.get("month_category")
            date_id = body.get("date_id")
            new_category = body.get("category")
            new_amount = body.get("amount")
            new_note = body.get("note", "")

            if not (month_category and date_id):
                return response(400, {"error": "Missing required keys for update"})

            result = update_expense(month_category, date_id, new_category, new_amount, new_note)
            return response(200, result)

        # ✅ DELETE EXPENSE
        elif http_method == "DELETE" and "/expenses" in path:
            month_category = params.get("month_category")
            date_id = params.get("date_id")

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




 








    
    
      
      