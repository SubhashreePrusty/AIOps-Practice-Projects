# Project - Birthday Tracker 🎂

#### This application helps you track birthdays of your friends and send alerts.

## Features:
- Add, view, and delete birthdays.
- Receive email alerts (11:00pm IST) for upcoming birthdays and (9:00am IST) for current birthdays.


## Folder Structure of the project

```
birthday-tracker/
│
├── .gitignore
├── requirements.txt
├── README.md
├── .env                        
│
├── venv/                  
│
├── streamlit_app/
│   ├── app.py                  
│   ├── api_client.py  
│   ├── next_birthday.py                  
│   ├── view_birthday.py           
│   └── utils.py                
│
├── lambda_functions/               # (Codes should be tested in the AWS lambda consoles)
│   ├── add_birthday/
│   │   └── app.py              
│   ├── get_birthdays/
│   │   └── app.py             
│   ├── delete_birthday/
│   │   └── app.py              
│   └── daily_reminder/
│       └── app.py              

```

### .env format

```
API_URL=
DYNAMODB_TABLE=
SNS_TOPIC_ARN=
```

## Featured Demonstrations




