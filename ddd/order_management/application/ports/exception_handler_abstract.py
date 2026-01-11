from __future__ import annotations
from typing import Protocol
from ddd.order_management.application import dtos

class ExceptionHandlerAbstract(Protocol):
    """Port for handling exceptions and logging, returning a standard ResponseDTO."""
    
    #Handle expected business logic errors (warnings/info logs)
    def handle_expected(self, exception: Exception) -> dtos.ResponseDTO: ...
        
    #Handle unexpected system errors (error logs, full traceback).
    def handle_unexpected(self, exception: Exception) -> dtos.ResponseDTO: ...
