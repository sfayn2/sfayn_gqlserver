from __future__ import annotations
from order_management import models as django_snapshots
from ddd.order_management.application import ports

class DjangoTenantWorkflowSnapshotRepo(ports.SnapshotRepoAbstract):

    def sync(self, event: dtos.TenantWorkflowUpdateIntegrationEvent):
        django_snapshots.TenantWorkflowSnapshot.objects.update_or_create(
            tenant_id=event.data.tenant_id, 
            vendor_id=event.data.vendor_id, 
            offer_id=event.data.offer_id,
            defaults=event.model_dump().get("data")
        )

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



