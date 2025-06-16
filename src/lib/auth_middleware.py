import json
import boto3
from botocore.exceptions import ClientError

def require_auth(handler):
    def wrapper(event, context):
        try:
            headers = event.get('headers', {})
            auth_header = headers.get('Authorization')

            if not auth_header:
                return {
                    'statusCode': 401,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({
                        'message': 'No authorization header'
                    })
                }

            token = auth_header.replace('Bearer ', '')

            client = boto3.client('cognito-idp')
            user_info = client.get_user(
                AccessToken=token
            )
            event['user'] = user_info

            return handler(event, context)

        except ClientError as e:
            error_message = e.response['Error']['Message']
            return {
                'statusCode': 401,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': error_message
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': f'Internal server error: {str(e)}'
                })
            }
    
    return wrapper