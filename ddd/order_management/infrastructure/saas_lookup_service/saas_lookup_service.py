from __future__ import annotations
import json
from typing import List, Dict, Any
from order_management import models as django_models

from ddd.order_management.domain import enums
from ddd.order_management.application import dtos

#Protocol: ports.LookupServiceAbstract
class SaaSLookupService:
    def get_tenant_config(
        self,
        tenant_id: str
    ) -> dtos.TenantDTO:
        try:
            tenant = django_models.SaaSConfig.objects.get(
                tenant_id=tenant_id
            )
        except django_models.SaaSConfig.DoesNotExist:
            raise Exception(f"Tenant {tenant_id} not found")

        return dtos.TenantDTO(
            tenant_id=tenant_id,
            configs=json.loads(tenant.configs)
        )