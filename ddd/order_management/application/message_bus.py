
from typing import Union, Dict, Callable, Any
from ddd.order_management.application import commands, queries
from ddd.order_management.domain import repositories

COMMAND_HANDLERS: Dict[commands.Command, Callable[..., Any]] = {}

QUERY_HANDLERS: Dict[queries.Query, Callable[..., Any]] = {}


def handle(message: Union[commands.Command, queries.Query], **deps):
    """ dispatch message to appropriate handler(s) """
    if isinstance(message, commands.Command):
        handler = COMMAND_HANDLERS.get(type(message))
        if not handler:
            raise ValueError(f"No handler registered for command: {type(message)}")

        results = handler(message, **deps)

        #made this cross cutting
        user_ctx = deps.get("user_ctx") 
        user_action_service = deps.get("user_action_service") 
        if results.success == True and user_ctx and user_action_service:
            user_action_service.save_action(
                order_id=getattr(message, "order_id", None),
                action=type(message).__name__,
                performed_by=user_ctx.sub,
                user_input=message.model_dump(exclude_none=True)
            )

        return results
    elif isinstance(message, queries.Query):
        handler = QUERY_HANDLERS.get(type(message))
        if not handler:
            raise ValueError(f"No handler registered for query: {type(message)}")
        results = handler(message, **deps)
        return results
    else:
        raise ValueError(f"Unknown message type {type(message)}")
