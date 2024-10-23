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
# DELETE: Menghapus to-do berdasarkan id
        if event['routeKey'] == "DELETE /todos/{id}":
            table.delete_item(
                Key={'id': event['pathParameters']['id']}
            )
            body = {'message': 'Deleted to-do ' + event['pathParameters']['id']}

        # GET: Mendapatkan satu to-do berdasarkan id
        elif event['routeKey'] == "GET /todos/{id}":
            response = table.get_item(
                Key={'id': event['pathParameters']['id']}
            )
            body = response.get("Item", {})
            if body:
                responseBody = {'id': body['id'], 'task': body['task'], 'status': body['status']}
            else:
                responseBody = {'message': 'To-do item not found'}
            body = responseBody
       
        # GET: Mendapatkan semua to-do items
        elif event['routeKey'] == "GET /todos":
            response = table.scan()
            items = response.get("Items", [])
            responseBody = [{'id': item['id'], 'task': item['task'], 'status': item['status']} for item in items]
            body = responseBody
