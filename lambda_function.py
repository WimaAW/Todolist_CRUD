import json
import boto3
from decimal import Decimal
import uuid  # Untuk menghasilkan ID unik

# Inisialisasi client dan resource DynamoDB
client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('todo-list-items')  # Nama tabel DynamoDB untuk to-do list

def lambda_handler(event, context):
    print(event)  # Mencetak event untuk debugging
    body = {}
    statusCode = 200
    headers = {
        "Content-Type": "application/json"
    }

    try:
