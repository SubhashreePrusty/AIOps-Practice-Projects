# s3_backup.py
import boto3
import os
import pandas as pd
import io
from datetime import datetime, timedelta
from decimal import Decimal

# Initialize AWS clients
dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")

# Environment variables (set in Lambda configuration)
TABLE_NAME = os.environ["DYNAMODB_TABLE"]
BUCKET_NAME = os.environ["S3_BUCKET"]

table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    """
    This Lambda:
    ✅ Backs up last month's category-wise summary to S3.
    ✅ Deletes last month's data from DynamoDB.
    ✅ Keeps current month's data untouched.
    """
    try:
        # Step 1: Identify current + last month
        today = datetime.now()
        first_day_this_month = datetime(today.year, today.month, 1)
        last_month_date = first_day_this_month - timedelta(days=1)
        last_month = last_month_date.strftime("%Y-%m")

        print(f"🗓️ Starting backup for {last_month}")

        # Step 2: Fetch all data from DynamoDB
        scan_resp = table.scan()
        items = scan_resp.get("Items", [])
        print(f"Fetched {len(items)} total records from DynamoDB")

        # Step 3: Filter last month's data only
        last_month_items = [item for item in items if item["date"].startswith(last_month)]
        if not last_month_items:
            print(f"No data found for {last_month}. Nothing to back up.")
            return {"status": "no_data", "message": f"No records for {last_month}"}

        # Step 4: Prepare DataFrame for category-wise summary
        df = pd.DataFrame(last_month_items)
        df["amount"] = df["amount"].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
        summary_df = df.groupby("category", as_index=False)["amount"].sum()

        # Step 5: Convert summary to CSV and upload to S3
        csv_buffer = io.StringIO()
        summary_df.to_csv(csv_buffer, index=False)
        s3_key = f"summaries/{last_month}-summary.csv"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=csv_buffer.getvalue(),
            ContentType="text/csv"
        )

        print(f"✅ Uploaded summary to s3://{BUCKET_NAME}/{s3_key}")

        # Step 6: Delete last month's records from DynamoDB
        with table.batch_writer() as batch:
            for item in last_month_items:
                batch.delete_item(
                    Key={
                        "month_category": item["month_category"],
                        "date_id": item["date_id"]
                    }
                )

        print(f"🧹 Deleted {len(last_month_items)} records for {last_month}")

        return {"status": "success", "message": f"Backup complete for {last_month}"}

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"status": "error", "message": str(e)}
