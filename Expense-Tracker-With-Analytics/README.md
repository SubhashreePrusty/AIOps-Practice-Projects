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

personal_expense_tracker/
│
├── streamlit_app/                 # 🎨 Frontend layer
│   ├── app.py                     # Main Streamlit entry point
│   │── add_expense.py             # Add new expense page
│   │── view_expenses.py           # View / visualize expenses page
│   │── analytics.py               # Optional insights/charts
│   │── utils.py                   # Functions to call API Gateway endpoints
│
├── lambda_functions/              # ⚙️ Backend AWS Lambda code
│   ├── handler.py                 # Lambda entry point (main)
│   ├── db_operations.py           # DynamoDB CRUD operations
│   ├── s3_backup.py               # (Optional) Weekly CSV backup logic
│   └── utils.py                   # Common backend utilities
│   └── delete_expense.py          
│   └── edit_expense.py            
│
├── .env.example                   # Template for environment variables
├── .gitignore                     # Ignore unnecessary files
├── requirements.txt               # Main dependencies for Streamlit app
├── README.md                      # Project overview and setup steps
└── venv/                          # 🧩 Virtual environment folder


```