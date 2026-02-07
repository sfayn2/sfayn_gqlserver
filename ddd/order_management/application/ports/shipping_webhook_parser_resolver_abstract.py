from __future__ import annotations
from typing import Dict, Any, Optional, Protocol
from ddd.order_management.application import dtos

class ShippingWebhookParserResolverAbstract(Protocol):
    def parse(cls, tenant_id: str, raw_body: bytes, order_id: str) -> dtos.ShippingWebhookRequestDTO: ...
