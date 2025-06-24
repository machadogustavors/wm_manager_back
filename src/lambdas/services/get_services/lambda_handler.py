import json

from src.lib.dynamo_connection import DynamoConnection
from src.lib.utils import DecimalEncoder, DynamoDBConverter
from src.lib.auth_middleware import require_auth

from src.lambdas.services.get_services.schema import Service

db = DynamoConnection()

@require_auth
def lambda_handler(event, context):
    try:
        items = db.get_all_items('servicos')

        py_items = [DynamoDBConverter.from_dynamo_format(item) for item in items]

        services = [Service(**item) for item in py_items]
        
        service_dict = [service.model_dump() for service in services]

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(service_dict, cls=DecimalEncoder)
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