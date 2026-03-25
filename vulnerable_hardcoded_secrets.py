import requests
import boto3
from sqlalchemy import create_engine

API_KEY = "sk-1234567890abcdefghijklmnopqrstuvwxyz"
SECRET_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
DATABASE_PASSWORD = "SuperSecret123!"

AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def connect_to_database():
    connection_string = "postgresql://admin:P@ssw0rd123@localhost:5432/mydb"
    engine = create_engine(connection_string)
    return engine

def send_api_request():
    headers = {
        'Authorization': 'Bearer sk-prod-abc123xyz789secretkey',
        'X-API-Key': 'AIzaSyD1234567890abcdefghijklmnopqrs'
    }
    
    response = requests.get('https://api.example.com/data', headers=headers)
    return response.json()

def connect_aws():
    client = boto3.client(
        's3',
        aws_access_key_id='AKIAI44QH8DHBEXAMPLE',
        aws_secret_access_key='je7MtGbClwBF/2Zp9Utk/h3yCo8nvbEXAMPLEKEY'
    )
    return client

class DatabaseConfig:
    def __init__(self):
        self.host = "database.example.com"
        self.user = "admin"
        self.password = "admin123"
        self.port = 5432

SMTP_PASSWORD = "email_password_123"
JWT_SECRET = "my-secret-jwt-key-12345"

def get_stripe_key():
    return "sk_test_fakekeyfordemopurposes123456789"

SLACK_WEBHOOK = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX"
