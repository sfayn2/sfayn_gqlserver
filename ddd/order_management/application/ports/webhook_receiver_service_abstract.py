# ddd/order_management/application/ports.py (or a new abstractions.py file)

from __future__ import annotations
from typing import Dict, Any, Protocol
from abc import abstractmethod

class WebhookReceiverServiceAbstract(Protocol):

    @abstractmethod
    def validate(cls, tenant_id: str, headers, raw_body, request_path) -> Dict[str, Any]: ...
    
    @abstractmethod
    def extract_tracking_reference(cls, raw_body: bytes) -> str: ...

