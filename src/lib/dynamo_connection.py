import os
import boto3

class DynamoConnection:
    def __init__(self):
        self.dynamo = boto3.resource(
            'dynamodb',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
            region_name=os.getenv('AWS_REGION')
        )

    def get_all_items(self, table_name):
        try:
            table = self.dynamo.Table(table_name)
            response = table.scan()
            items = response['Items']

            while 'LastEvaluatedKey' in response:
                response = table.scan(
                    ExclusiveStartKey = response['LastEvaluatedKey']
                )
                items.extend(response['Items'])

            return items
        
        except Exception as e:
            print('Error: ', str(e))
            raise

    def create_item(self, table_name, item):
        try:
            table = self.dynamo.Table(table_name)
            response = table.put_item(Item=item)

            return response
        except Exception as e:
            print('Error: ', str(e))
            raise

    def delete_item(self, table_name, key):
        try:
            table = self.dynamo.Table(table_name)
            response = table.delete_item(Key=key)
            return response
            
        except Exception as e:
            print('Error: ', str(e))
            raise

    def update_item(self, table_name, key, attributes: dict):
        try:
            table = self.dynamo.Table(table_name)
            
            attributes = {k: v for k, v in attributes.items() if v is not None}
            
            update_expression = "SET " + ", ".join(f"#{k} = :{k}" for k in attributes)
            expression_names = {f"#{k}": k for k in attributes}
            expression_values = {f":{k}": v for k, v in attributes.items()}
            
            response = table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_names,
                ExpressionAttributeValues=expression_values,
                ReturnValues="ALL_NEW"
            )
            
            return response.get('Attributes')
            
        except Exception as e:
            print('Error: ', str(e))
            raise