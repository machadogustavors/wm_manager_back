import json

from src.lib.dynamo_connection import DynamoConnection

db = DynamoConnection()

def lambda_handler(event, context):
    try:
        service_id = event['pathParameters']['id']
        
        result = db.delete_item('servicos', {'id_servico': service_id})
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': f'Service {service_id} deleted successfully'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }