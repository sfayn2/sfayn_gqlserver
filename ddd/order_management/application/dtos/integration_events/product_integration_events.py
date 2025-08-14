import uuid
from decimal import Decimal
from pydantic import BaseModel, root_validator, Field
from typing import Dict, Optional, List
from ddd.order_management.application import dtos
from .base import IntegrationEvent

class ProductUpdateIntegrationEvent(IntegrationEvent):
    #event_type: str
    data: dtos.VendorProductSnapshotDTO


