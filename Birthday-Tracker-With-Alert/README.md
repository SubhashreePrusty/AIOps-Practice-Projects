```
python -m venv venv
venv\Scripts\activate
streamlit run streamlit_app/app.py
```

If there is a problem to create the virtual environment, run this command -
#### Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

To revert later - 
#### Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope CurrentUser


```
birthday-tracker/
│
├── .gitignore
├── requirements.txt
├── README.md
├── .env                        # (optional, for API URL, region, etc.)
│
├── venv/                       # Virtual environment (created locally)
│
├── streamlit_app/
│   ├── app.py                  # Main Streamlit frontend
│   ├── api_client.py           # Functions that call AWS API Gateway
│   └── utils.py                # Helper functions (e.g., date formatting)
│
├── lambda_functions/
│   ├── add_birthday/
│   │   └── app.py              # Lambda for adding new birthdays
│   ├── get_birthdays/
│   │   └── app.py              # Lambda for viewing birthdays
│   ├── delete_birthday/
│   │   └── app.py              # Lambda for deleting a record
│   └── daily_reminder/
│       └── app.py              # Lambda triggered daily by EventBridge
│
├── infrastructure/
│   ├── create_dynamodb_table.py   # (Optional) boto3 script to create DynamoDB table
│   ├── create_sns_topic.py        # (Optional) to create SNS topic
│   └── deploy_lambda.sh           # (Optional) helper script for zipping & uploading Lambdas
│
└── tests/
    └── test_sample.py          # (Optional) Unit tests for core logic


```