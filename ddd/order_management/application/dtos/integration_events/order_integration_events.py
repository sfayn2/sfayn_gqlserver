from __future__ import annotations
import uuid
from pydantic import BaseModel, root_validator, Field
from typing import Dict, Optional, List
from .base import IntegrationEvent
from ddd.order_management.application import dtos


class ConfirmedShipmentIntegrationEvent(IntegrationEvent):
    tenant_id: str
    order_id: str
    shipment_id: str
    order_status: enums.OrderStatus

