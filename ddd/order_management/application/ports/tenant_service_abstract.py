from __future__ import annotations
from typing import Protocol

class TenantServiceAbstract(Protocol):
    def get_tenant_config(
        self,
        tenant_id: str
    ) -> dtos.TenantDTO:
        ...
