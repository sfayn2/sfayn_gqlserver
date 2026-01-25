from __future__ import annotations
import json
from typing import List, Dict, Any
from order_management import models as django_models

from ddd.order_management.domain import enums
from ddd.order_management.application import dtos

class TenantLookupException(Exception):
    """Unified exception for Tenant Lookup Service failures."""
    pass

#Protocol: ports.LookupServiceAbstract
class TenantLookupService:
    def get_tenant_config(
        self,
        tenant_id: str
    ) -> dtos.TenantResponseDTO:
        try:
            tenant = django_models.TenantConfig.objects.get(
                tenant_id=tenant_id
            )
        except django_models.TenantConfig.DoesNotExist:
            raise TenantLookupException(f"TenantLookupService: Tenant {tenant_id} not found")

        return dtos.TenantResponseDTO(
            tenant_id=tenant_id,
            configs=json.loads(tenant.configs)
        )