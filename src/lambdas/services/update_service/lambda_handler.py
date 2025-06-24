import json

from src.lib.dynamo_connection import DynamoConnection
from src.lib.utils import DecimalEncoder

from src.lambdas.services.update_service.schema import UpdateServiceRequest

db = DynamoConnection()

def lambda_handler(event, context):
    try:
        service_id = event['pathParameters']['id']
        
        body = json.loads(event['body'])
        
        service_request = UpdateServiceRequest(**body)
        
        updates = service_request.model_dump(exclude_unset=True)
        
        result = db.update_item(
            'servicos',
            {'id_servico': service_id},
            updates
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result, cls=DecimalEncoder)
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