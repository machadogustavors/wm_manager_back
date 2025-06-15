from pydantic import BaseModel
from typing import Optional
from datetime import date as Date
from decimal import Decimal

class ServiceBase(BaseModel):
    date: Optional[Date] = None
    client_name: Optional[str] = None
    car_model: Optional[str] = None
    license_plate: Optional[str] = None
    parts_cost: Optional[Decimal] = None
    labor_cost: Optional[Decimal] = None
    mechanic: Optional[str] = None
    service_description: Optional[str] = None
    payment: Optional[str] = None