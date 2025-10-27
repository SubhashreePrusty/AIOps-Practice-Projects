import json
import boto3
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
import os

sns = boto3.client("sns")
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.getenv("DYNAMODB_TABLE")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    try:
        reminder_type = event.get("reminder_type", "morning_of")
        now = datetime.now().date()  # force UTC date
        today = now
        tomorrow = today + timedelta(days=1)

        print(f"🕒 Current UTC date={today}, checking for reminder_type={reminder_type}")

        resp = table.scan()
        items = resp.get("Items", [])
        reminders = []

        for item in items:
            bday_str = item.get("birthday")
            name = item.get("name")

            if not bday_str or not name:
                continue

            try:
                # Force to date only (strip time and tz)
                bday = parse_date(bday_str).date()
            except Exception as e:
                print(f"❌ Failed to parse {bday_str}: {e}")
                continue

            print(f"🔍 Checking {name}: {bday} → (month={bday.month}, day={bday.day}) vs today={today}, tomorrow={tomorrow}")

            # Compare month/day explicitly
            if reminder_type == "morning_of" and (bday.month, bday.day) == (today.month, today.day):
                reminders.append(f"🎂 Today is {name}'s birthday!")
            elif reminder_type == "night_before" and (bday.month, bday.day) == (tomorrow.month, tomorrow.day):
                reminders.append(f"🎉 Tomorrow is {name}'s birthday!")

        if reminders:
            message = "\n".join(reminders)
            print("🎉 Sending SNS alert for these reminders:")
            for msg in reminders:
                print(f"   - {msg}")

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=message,
                Subject="🎉 Birthday Reminder Alert!",
            )

            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Reminders sent!", "details": reminders})
            }
        else:
            print("ℹ️ No birthdays matched after normalization.")
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "No birthdays to remind today"})
            }

    except Exception as e:
        print(f"❌ Exception: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
