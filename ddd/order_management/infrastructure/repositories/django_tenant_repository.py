from __future__ import annotations
import json
from typing import List, Dict, Any
from order_management import models as django_models

from ddd.order_management.domain import enums

#Protocol: ports.TenantSnapshotAbstract
class DjangoTenantSnapshotRepository:
    def get_tenant_config(
        self,
        tenant_id: str
    ):
        return django_models.TenantSnapshot.objects.get(
            tenant_id=tenant_id
        )