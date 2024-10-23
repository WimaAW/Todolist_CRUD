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

        # PUT: Menambah atau memperbarui to-do item
        elif event['routeKey'] == "PUT /todos":
            requestJSON = json.loads(event['body'])
            task_id = str(uuid.uuid4())  # Membuat ID unik untuk setiap tugas
            table.put_item(
                Item={
                    'id': task_id,
                    'task': requestJSON['task'],  # Deskripsi tugas dari request body
                    'status': 'pending'  # Status default saat ditambahkan adalah pending
                }
            )
            body = 'Put item ' + task_id  # Mengubah response agar lebih sederhana


        # POST: Memperbarui status to-do (misal: completed)
        elif event['routeKey'] == "POST /todos/{id}/complete":
            table.update_item(
                Key={'id': event['pathParameters']['id']},
                UpdateExpression="set #s = :status",
                ExpressionAttributeNames={"#s": "status"},
                ExpressionAttributeValues={":status": "completed"}
            )
            body = {'message': 'Updated to-do status to completed for ' + event['pathParameters']['id']}
            
    except KeyError:
        statusCode = 400
        body = {'message': 'Unsupported route: ' + event['routeKey']}
    
    # Menyiapkan response untuk dikembalikan
    body = json.dumps(body)
    res = {
        "statusCode": statusCode,
        "headers": headers,
        "body": body
    }
    return res
