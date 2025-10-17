from __future__ import annotations
import json
from typing import List, Dict, Any
from order_management import models as django_models

from ddd.order_management.domain import enums
from ddd.order_management.application import dtos

#Protocol: ports.TenantServiceAbstract
class TenantService:
    def get_tenant_config(
        self,
        tenant_id: str
    ) -> dtos.TenantDTO:
        try:
            tenant = django_models.TenantSnapshot.objects.get(
                tenant_id=tenant_id
            )
        except django_models.TenantSnapshot.DoesNotExist:
            raise Exception(f"Tenant {tenant_id} not found")

        return dtos.TenantDTO(
            tenant_id=tenant_id,
            config=json.loads(tenant.config)
        )