import json
import datetime

from src.lib.dynamo_connection import DynamoConnection
from src.lib.utils import DecimalEncoder
from src.lib.auth_middleware import require_auth

from src.lambdas.services.update_service.schema import UpdateServiceRequest

db = DynamoConnection()

@require_auth
def lambda_handler(event, context):
    try:
        service_id = event['pathParameters']['id']
        
        body = json.loads(event['body'])
        
        service_request = UpdateServiceRequest(**body)
        
        updates = service_request.model_dump(exclude_unset=True)
        
        for k, v in updates.items():
            if isinstance(v, (datetime.date, datetime.datetime)):
                updates[k] = v.isoformat()
        
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