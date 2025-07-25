import json
import boto3
import os
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        username = body.get('username')
        password = body.get('password')
        
        client = boto3.client('cognito-idp')
        
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            ClientId=os.getenv('COGNITO_CLIENT_ID'),
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )

        access_token = response['AuthenticationResult']['AccessToken']
        user_info = client.get_user(AccessToken=access_token)
        email = None
        for attr in user_info['UserAttributes']:
            if attr['Name'] == 'email':
                email = attr['Value']
                break
            
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'Successfully authenticated',
                'email': email,
                'tokens': {
                    'AccessToken': response['AuthenticationResult']['AccessToken'],
                    'IdToken': response['AuthenticationResult']['IdToken'],
                    'RefreshToken': response['AuthenticationResult']['RefreshToken']
                }
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