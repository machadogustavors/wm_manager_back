from pydantic import computed_field
from decimal import Decimal
from typing import Optional
from datetime import date as Date, datetime

from src.lib.models import ServiceBase

class Service(ServiceBase):
    id_servico: str
    created_at: datetime
    date: Optional[Date] = None

    @computed_field
    @property
    def total_cost(self) -> Decimal:
        parts = self.parts_cost or Decimal('0')
        labor = self.labor_cost or Decimal('0')
        return parts + labor
    
    @computed_field
    @property
    def parts_store_cost(self) -> Decimal:
        parts = self.parts_cost or Decimal('0')
        return parts * Decimal('0.52')
    
    @computed_field
    @property
    def parts_store_profit(self) -> Decimal:
        parts = self.parts_cost or Decimal('0')
        return parts * Decimal('0.48')