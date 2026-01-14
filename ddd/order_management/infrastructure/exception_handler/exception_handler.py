from __future__ import annotations
import logging
import traceback
from ddd.order_management.application import ports, dtos
from ddd.order_management.domain import exceptions

logger = logging.getLogger(__name__)


#ports.ExceptionHandlerAbstract
class OrderExceptionHandler:

    def handle_expected(self, exception: Exception) -> dtos.ResponseDTO:
        # Log this at a WARNING level, no traceback needed
        logger.warning(f"Business Rule Violation: {exception}")
        print(f"Business Rule Violation: {exception}")
        
        # This mirrors what you had in shared.handle_invalid_order_operation
        # You would add logic here to map specific exception types to generic error messages
        message = str(exception) 
        return dtos.ResponseDTO(success=False, message=message)

    def handle_unexpected(self, exception: Exception) -> dtos.ResponseDTO:
        # Log this at an ERROR level with full traceback
        logger.error(f"CRITICAL SYSTEM FAILURE: {exception}", exc_info=True)
        print(f"CRITICAL SYSTEM FAILURE: {traceback.format_exc()}")
        
        # Return a generic, safe error message to the user
        msg = "The Order Management service is temporarily unavailable. \n" \
            "Our team has been notified. Please try again in a few moments."
        return dtos.ResponseDTO(success=False, message=msg)

