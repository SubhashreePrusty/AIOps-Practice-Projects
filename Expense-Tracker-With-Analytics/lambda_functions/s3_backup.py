import boto3
import os
import csv
import io
from datetime import datetime, timedelta
from collections import defaultdict

# Initialize clients
dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")

TABLE_NAME = os.environ["DYNAMODB_TABLE"]
BUCKET_NAME = os.environ["S3_BUCKET"]
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    # 1️⃣ Get the last month string like "2025-09"
    today = datetime.utcnow().date()
    first_day_this_month = today.replace(day=1)
    last_month_date = first_day_this_month - timedelta(days=1)
    last_month_str = last_month_date.strftime("%Y-%m")

    print(f"📦 Starting backup for {last_month_str}")

    # 2️⃣ Fetch all records from DynamoDB
    response = table.scan()
    items = response.get("Items", [])

    # 3️⃣ Filter last month's records
    last_month_items = [
        item for item in items
        if item.get("date", "").startswith(last_month_str)
    ]

    if not last_month_items:
        print("No records found for last month. Exiting.")
        return {"statusCode": 200, "body": "No data to backup."}

    # 4️⃣ Summarize category-wise
    summary = defaultdict(float)
    for item in last_month_items:
        category = item.get("category", "Uncategorized")
        amount = float(item.get("amount", 0))
        summary[category] += amount

    # 5️⃣ Generate CSV content (category, total)
    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["Category", "Total Amount"])
    for cat, total in summary.items():
        writer.writerow([cat, total])

    csv_data = csv_buffer.getvalue()

    # 6️⃣ Upload to S3 (inside folder named after month)
    s3_key = f"{last_month_str}/category_summary_{last_month_str}.csv"
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=csv_data,
        ContentType="text/csv"
    )

    print(f"✅ Uploaded summary CSV to s3://{BUCKET_NAME}/{s3_key}")

    # 7️⃣ Delete old month data from DynamoDB
    with table.batch_writer() as batch:
        for item in last_month_items:
            batch.delete_item(
                Key={
                    "month_category": item["month_category"],
                    "date_id": item["date_id"]
                }
            )

    print(f"🧹 Deleted {len(last_month_items)} records from DynamoDB for {last_month_str}")


    return {
        "statusCode": 200,
        "body": f"Backup completed and {len(last_month_items)} records deleted for {last_month_str}"
    }
