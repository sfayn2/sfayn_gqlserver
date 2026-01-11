from __future__ import annotations
from typing import Protocol, Any, Type
from ddd.order_management.application import ports


class AccessControlServiceAbstract(Protocol):
    """
    Abstraction for the AccessControlService factory itself.
    """

    @classmethod
    def create_access_control(cls, tenant_id: str) -> ports.AccessControl1Abstract: ...

    # We don't expose private methods like _create_jwt_handler_for_tenant in the public protocol
    # The 'configure' and internal methods should not be part of the application port
