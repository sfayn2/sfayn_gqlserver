

from __future__ import annotations
from typing import Union
from ddd.order_management.application import (
    mappers, 
    commands, 
    ports, 
    dtos, 
    shared
)
from ddd.order_management.domain import exceptions

def handle_login_callback(
        command: commands.LoginCallbackCommand, 
        uow: UnitOfWorkAbstract, 
        login_callback_service: LoginCallbackServiceAbstract
    ) -> dtos.IdPTokenDTO:

    tokens = login_callback_service.get_tokens(command.code, command.redirect_uri)

    return tokens