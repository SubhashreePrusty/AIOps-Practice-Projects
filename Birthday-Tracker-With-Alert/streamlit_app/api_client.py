# Functions that call AWS API Gateway
import requests

def add_birthday(name, date):
    payload = {"name": name, "birthday": date}
    # response = requests.post(f"{API_BASE_URL}/add_birthday", json=payload)
    return payload.json()

