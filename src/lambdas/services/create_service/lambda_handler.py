import uuid
import json

from datetime import datetime

from src.lib.dynamo_connection import DynamoConnection
from src.lib.utils import DecimalEncoder, DynamoDBConverter
from src.lib.auth_middleware import require_auth

from src.lambdas.services.create_service.schema import CreateServiceRequest

db = DynamoConnection()

@require_auth
def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        service_request = CreateServiceRequest(**body)

        item = service_request.model_dump()

        item.update({
            'id_servico': str(uuid.uuid4()),
            'created_at': datetime.now()
        })

        dynamo_item = DynamoDBConverter.to_dynamo_format(item)
        
        result = db.create_item('servicos', dynamo_item)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(item, cls=DecimalEncoder)
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