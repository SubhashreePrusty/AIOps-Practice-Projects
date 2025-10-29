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

#### User Interface

<img width="1920" height="1128" alt="ui1" src="https://github.com/user-attachments/assets/7eb49c7f-c4f4-44b8-9e38-c3555df61cad" />

<img width="1920" height="1128" alt="ui2" src="https://github.com/user-attachments/assets/c8d13cdf-c000-4c56-a47b-be5a310323fa" />

#### DynamoDB Table

<img width="1920" height="1128" alt="dynamoDB_table" src="https://github.com/user-attachments/assets/9c6e8640-8ccf-40e3-9138-69c448cef2d6" />

#### Lambda Functions

<img width="1920" height="1128" alt="lambda_functions" src="https://github.com/user-attachments/assets/e66d7431-16f9-47cb-be55-3de156f4acb5" />

#### Demo add_birthday endpoint

<img width="1920" height="1128" alt="add_birthday_endpoint" src="https://github.com/user-attachments/assets/ce9ad3e1-6c47-41d4-bd78-39dccc4125ad" />

#### SNS Topic

<img width="1920" height="1128" alt="sns_topic" src="https://github.com/user-attachments/assets/1c44da26-485d-4ca0-9f7b-a3e6dff8d807" />

#### ------ END ------
