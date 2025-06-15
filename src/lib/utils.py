import json

from decimal import Decimal
from datetime import date, datetime
from typing import Dict, Any

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super(DecimalEncoder, self).default(obj)
    
class DynamoDBConverter:
    @staticmethod
    def to_dynamo_format(data: Dict[str, Any]) -> Dict[str, Any]:
        formatted_data = data.copy()
        
        for key, value in formatted_data.items():
            if isinstance(value, (date, datetime)):
                formatted_data[key] = value.isoformat()
            elif isinstance(value, Decimal):
                formatted_data[key] = str(value)
            elif value is None:
                del formatted_data[key]
                
        return formatted_data

    @staticmethod
    def from_dynamo_format(data: Dict[str, Any]) -> Dict[str, Any]:
        formatted_data = data.copy()
        
        try:
            if 'date' in formatted_data and formatted_data['date']:
                formatted_data['date'] = date.fromisoformat(formatted_data['date'])
            
            if 'created_at' in formatted_data and formatted_data['created_at']:
                formatted_data['created_at'] = datetime.fromisoformat(formatted_data['created_at'])
            
            for decimal_field in ['parts_cost', 'labor_cost']:
                if decimal_field in formatted_data and formatted_data[decimal_field]:
                    formatted_data[decimal_field] = Decimal(str(formatted_data[decimal_field]))
                    
        except (ValueError, TypeError) as e:
            print(f"Error converting types: {e}")
            raise
                
        return formatted_data