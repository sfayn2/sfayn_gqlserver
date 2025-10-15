from __future__ import annotations
from typing import Protocol

class TenantSnapshotAbstract(Protocol):
    def get_tenant_config(
        self,
        tenant_id: str
    ):
        ...
