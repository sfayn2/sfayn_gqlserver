from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod
from ddd.order_management.domain import value_objects

class TenantAbstract(ABC):

    @abstractmethod
    def get_tenant_workflow(
        self,
        tenant_id: str,
    ) -> List[dtos.TenantWorkflowSnapshotDTO]:
        raise NotImplementedError("Subclasses must implement this method")

    def sync(self, event: dtos.TenantWorkflowUpdateIntegrationEvent):
        raise NotImplementedError("Subclasses must implement this method")

