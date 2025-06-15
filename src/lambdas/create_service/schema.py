from datetime import datetime, date
from decimal import Decimal

from src.lib.models import ServiceBase

class CreateServiceRequest(ServiceBase):
    class Config:
        json_encoders = {
            Decimal: str,
            datetime: lambda dt: dt.isoformat(),
            date: lambda d: d.isoformat()
        }