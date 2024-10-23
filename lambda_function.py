import json
import boto3
from decimal import Decimal
import uuid  # Untuk menghasilkan ID unik

# Inisialisasi client dan resource DynamoDB
client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('todo-list-items')  # Nama tabel DynamoDB untuk to-do list

