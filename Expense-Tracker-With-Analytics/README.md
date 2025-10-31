# Project - Expense Tracker 💸📊

#### This application helps you track your expenses.

## Features:
- Add, view, edit and delete expenses.
- Category-wise summaries, analytics-charts.


## Folder Structure of the project

```
personal_expense_tracker/
│
├── streamlit_app/                 
│   ├── app.py                      
│   │── add_expense.py             
│   │── view_expenses.py 
│   └── delete_expense.py    
│   └── edit_expense.py       
│   │── analytics.py               
│   │── utils.py                   
│
├── lambda_functions/               # (Codes should be tested in the AWS lambda consoles)  
│   ├── lambda_functions.py                
│   ├── db_operations.py           
│   ├── s3_backup.py               
│   └── utils.py                              
│
├── .env                    
├── .gitignore                     
├── requirements.txt               
├── README.md                      
└── venv/                          

```

### .env format

```
API_URL=
DYNAMODB_TABLE=
S3_BUCKET=
```

## Featured Demonstrations



#### ------ END ------