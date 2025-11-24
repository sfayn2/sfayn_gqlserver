from __future__ import annotations
from typing import Protocol
from ddd.order_management.application import dtos

class LookupServiceAbstract(Protocol):
    def get_tenant_config(
        self,
        tenant_id: str
    ) -> dtos.TenantDTO:
        ...
