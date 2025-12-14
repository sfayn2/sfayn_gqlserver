from __future__ import annotations
import uuid
from pydantic import BaseModel, root_validator, Field
from typing import Dict, Optional, List
from .base import IntegrationEvent
from ddd.order_management.application import dtos


class ConfirmedShipmentIntegrationEvent(IntegrationEvent):
     # This data is an input request payload, so use the RequestDTO type
    data: dtos.ConfirmShipmentRequestDTO
    

class AddOrderWebhookIntegrationEvent(IntegrationEvent):
     # This data is an input request payload, so use the RequestDTO type
    data: dtos.AddOrderRequestDTO


class ShippingWebhookIntegrationEvent(IntegrationEvent):
     # This data is an input request payload, so use the RequestDTO type
    data: dtos.ShippingWebhookRequestDTO
