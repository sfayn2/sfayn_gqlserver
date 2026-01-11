from __future__ import annotations
import uuid
from pydantic import BaseModel
from typing import Dict, Optional, List
from .base import IntegrationEvent
from ddd.order_management.application import dtos

class AddOrderIntegrationDTO(BaseModel):
    external_ref: str
    tenant_id: str
    customer_details: dtos.CustomerDetailsRequestDTO
    product_skus: List[dtos.ProductSkusRequestDTO]


class ConfirmedShipmentIntegrationEvent(IntegrationEvent):
     # This data is an input request payload, so use the RequestDTO type
    data: dtos.ConfirmShipmentRequestDTO
    

class AddOrderWebhookIntegrationEvent(IntegrationEvent):
     # This data is an input request payload, so use the RequestDTO type
    data: AddOrderIntegrationDTO


class ShippingWebhookIntegrationEvent(IntegrationEvent):
     # This data is an input request payload, so use the RequestDTO type
    data: dtos.ShippingWebhookRequestDTO
