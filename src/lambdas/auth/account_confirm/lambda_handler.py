import json
import boto3
import os
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        username = body.get('username')
        confirmation_code = body.get('confirmation_code')

        if not all([username, confirmation_code]):
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': 'Username and confirmation code are required'
                })
            }

        client = boto3.client('cognito-idp')

        response = client.confirm_sign_up(
            ClientId=os.environ['COGNITO_CLIENT_ID'],
            Username=username,
            ConfirmationCode=confirmation_code
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'Account confirmed successfully'
            })
        }

    except ClientError as e:
        error_message = e.response['Error']['Message']
        return {
            'statusCode': 400,
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