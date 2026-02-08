from __future__ import annotations
from typing import Dict, Any, Optional, Protocol
from ddd.order_management.application import dtos

class ShippingWebhookParserResolverAbstract(Protocol):
    def parse_provider_shipment_update(cls, tenant_id: str, order_id: str, raw_body: bytes) -> dtos.ShippingWebhookRequestDTO: ...
