# ddd/order_management/application/ports.py (or a new abstractions.py file)

from __future__ import annotations
from typing import Dict, Any, Protocol

class TrackingReferenceExtractorAbstract(Protocol):
    def extract_tracking_reference(cls, raw_body: bytes, saas_id: str) -> str: ...

