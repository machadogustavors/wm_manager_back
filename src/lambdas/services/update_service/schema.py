from datetime import date
from decimal import Decimal

from src.lib.models import ServiceBase

class UpdateServiceRequest(ServiceBase):
    class Config:
        json_encoders = {
            Decimal: str,
            date: lambda d: d.isoformat() if d else None
        }