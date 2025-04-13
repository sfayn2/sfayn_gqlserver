
from typing import Union, Dict, Callable
from ddd.order_management.application import commands, queries
from ddd.order_management.domain import repositories

COMMAND_HANDLERS: Dict[commands.Command, Callable] = {}

QUERY_HANDLERS: Dict[queries.Query, Callable] = {}

def handle(message: Union[commands.Command, queries.Query], uow: repositories.UnitOfWorkAbstract, dependencies: None):
    """ dispatch message to appropriate handler(s) """
    if isinstance(message, commands.Command):
        handler = COMMAND_HANDLERS.get(type(message))
        if not handler:
            raise ValueError(f"No handler registered for command: {type(message)}")
        results = handler(message, uow, **dependencies)
        return results
    elif isinstance(message, queries.Query):
        handler = QUERY_HANDLERS.get(type(message))
        if not handler:
            raise ValueError(f"No handler registered for query: {type(message)}")
        results = handler(message, uow, **dependencies)
        return results
    else:
        raise ValueError(f"Unknown message type {type(message)}")
