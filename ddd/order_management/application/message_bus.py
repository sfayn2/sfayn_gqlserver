
from __future__ import annotations
from typing import Union, Dict, Callable, Any, Optional
from ddd.order_management.application import commands, queries
from ddd.order_management.domain import repositories

COMMAND_HANDLERS: Dict[commands.Command, Callable[..., Any]] = {}

QUERY_HANDLERS: Dict[queries.Query, Callable[..., Any]] = {}

ACCESS_CONTROL_SERVICE_IMPL: Optional[ports.AccessControl1Abstract] = None


def handle(message: Union[commands.Command, queries.Query], **deps):
    """ dispatch message to appropriate handler(s) """
    if isinstance(message, commands.Command):
        handler = COMMAND_HANDLERS.get(type(message))
        if not handler:
            raise ValueError(f"No handler registered for command: {type(message)}")

        context_data: dtos.RequestContextDTO = deps.pop("context_data", None) 
        if context_data:
            if not ACCESS_CONTROL_SERVICE_IMPL:
                raise PermissionError("Access control service definition is required to authorize user.")

            access_control = ACCESS_CONTROL_SERVICE_IMPL.create_access_control(context_data.tenant_id)
            user_ctx = access_control.get_user_context(context_data.token, context_data.tenant_id)

            deps["access_control"] = access_control
            deps["user_ctx"] = user_ctx

        results = handler(message, **deps)

        return results
    elif isinstance(message, queries.Query):
        handler = QUERY_HANDLERS.get(type(message))
        if not handler:
            raise ValueError(f"No handler registered for query: {type(message)}")
        results = handler(message, **deps)
        return results
    else:
        raise ValueError(f"Unknown message type {type(message)}")
