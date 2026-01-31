from __future__ import annotations
from typing import Protocol, Optional
from ddd.order_management.application import ports


class ContextHeaderExtractorAbstract(Protocol):
    """
    Abstraction for the ContextHeaderExtractor factory itself.
    """
    def get_auth_header(cls, tenant_id: str) -> Optional[str]: ...
