import uuid
from decimal import Decimal
from pydantic import BaseModel, root_validator, Field
from typing import Dict, Optional, List
from ddd.order_management.application import dtos

class ProductUpdateIntegrationEvent(BaseModel):
    event_type: str
    data: dtos.VendorProductSnapshotDTO


