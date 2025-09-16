from __future__ import annotations
import pytz, uuid
from datetime import datetime
from typing import List
from ddd.order_management.domain import (
    repositories, 
    enums, 
    value_objects, 
    exceptions, 
    models
)
from order_management import models as django_snapshots
from ddd.order_management.infrastructure import django_mappers
from ddd.order_management.application import dtos, ports

class DjangoTenantWorkflowRepositoryImpl(ports.TenantAbstract):

    def get_tenant_workflow(
        self,
        tenant_id: str,
    ) -> List[dtos.TenantWorkflowSnapshotDTO]:
        tenant_workflow = django_snapshots.TenantWorkflowSnapshot.objects.filter(tenant_id=tenant_id, is_active=True)
        final_opts = []
        for option in tenant_workflow.values():
            try:
                final_opts.append(
                    django_mappers.OtherActivityMapper.to_domain(option)
                )
            except (ValueError) as e:
                print(f"DjangoVendorRepository.load_tenant_workflow exception > {str(e)}")
                continue
        return final_opts

