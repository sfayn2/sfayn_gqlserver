# ddd/order_management/application/ports.py (or a new abstractions.py file)

from __future__ import annotations
from typing import Dict, Any, Protocol

class WebhookReceiverServiceAbstract(Protocol):
    def validate_signature(cls, tenant_id: str, headers, raw_body, request_path, validator_dto) -> None: ...

