from __future__ import annotations
import uuid
from pydantic import BaseModel, root_validator, Field
from typing import Dict, Optional, List
from .base import IntegrationEvent
from ddd.order_management.application import dtos


class ConfirmedShipmentIntegrationEvent(IntegrationEvent):
    data: dtos.ConfirmShipmentDTO
    

class AddOrderIntegrationEvent(IntegrationEvent):
    data: dtos.AddOrderDTO