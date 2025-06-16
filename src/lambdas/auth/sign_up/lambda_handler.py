import json
import boto3
import os
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        username = body.get('username')
        password = body.get('password')
        email = body.get('email')
        phone_number = body.get('phone_number')
        birthdate = body.get('birthdate')

        if not all([username, password, email, phone_number, birthdate]):
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': 'All fields are required'
                })
            }

        client = boto3.client('cognito-idp')

        response = client.sign_up(
            ClientId=os.getenv('COGNITO_CLIENT_ID'),
            Username=username,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
                {
                    'Name': 'phone_number',
                    'Value': phone_number
                },
                {
                    'Name': 'birthdate',
                    'Value': birthdate
                }
            ]
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'User registration successful. Please check your email for verification code.',
                'userSub': response['UserSub']
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