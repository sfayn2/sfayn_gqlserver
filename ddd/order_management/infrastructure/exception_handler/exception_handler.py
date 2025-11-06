from __future__ import annotations
import logging
from ddd.order_management.application import ports, dtos

logger = logging.getLogger(__name__)

#ExceptionHandlerAbstract
class InfrastructureExceptionHandler:

    def handle_expected(self, exception: Exception) -> dtos.ResponseDTO:
        # Log this at a WARNING level, no traceback needed
        logger.warning(f"Handled expected application error: {exception}")
        
        # This mirrors what you had in shared.handle_invalid_order_operation
        # You would add logic here to map specific exception types to generic error messages
        message = str(exception) 
        return dtos.ResponseDTO(success=False, message=message)

    def handle_unexpected(self, exception: Exception) -> dtos.ResponseDTO:
        # Log this at an ERROR level with full traceback
        logger.error(f"UNEXPECTED SYSTEM ERROR: {exception}", exc_info=True)
        
        # Return a generic, safe error message to the user
        return dtos.ResponseDTO(success=False, message="An internal server error occurred.")

