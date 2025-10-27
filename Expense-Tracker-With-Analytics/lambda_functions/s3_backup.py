# Weekly CSV backup logic

import os
import csv
import io
import boto3
from db_operations import get_all_expenses

s3 = boto3.client("s3")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "expense-tracker-backup")

def lambda_handler(event, context):
    """Backup all expenses to S3 as a CSV"""
    items = get_all_expenses()
    if not items:
        return {"status": "info", "message": "No expenses to backup"}

    csv_buffer = io.StringIO()
    fieldnames = list(items[0].keys())
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(items)

    file_name = f"backup_{context.aws_request_id}.csv"
    s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=csv_buffer.getvalue())

    return {"status": "success", "message": f"Backup saved to s3://{BUCKET_NAME}/{file_name}"}
