from __future__ import annotations
from typing import Dict, Any, Protocol
from ddd.order_management.application import dtos
# Import the domain model type
from ddd.order_management.domain import models

class ShippingWebhookParserResolverAbstract(Protocol):
    @classmethod
    def resolve(cls, tenant_id: str, payload: Any) -> dtos.ShippingWebhookDTO: ...
    # The 'configure' and internal methods should not be part of the application port
