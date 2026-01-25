from __future__ import annotations
import json
from typing import List, Dict, Any
from order_management import models as django_models

from ddd.order_management.domain import enums
from ddd.order_management.application import dtos

class SaaSLookupException(Exception):
    """Unified exception for SaaS Lookup Service failures."""
    pass

#Protocol: ports.LookupServiceAbstract
class SaaSLookupService:
    def get_tenant_config(
        self,
        tenant_id: str
    ) -> dtos.TenantResponseDTO:
        try:
            tenant = django_models.SaaSConfig.objects.get(
                tenant_id=tenant_id
            )
        except django_models.SaaSConfig.DoesNotExist:
            raise SaaSLookupException(f"SaaSLookupService: SaaS Tenant {tenant_id} not found")

        return dtos.TenantResponseDTO(
            tenant_id=tenant_id,
            configs=json.loads(tenant.configs)
        )