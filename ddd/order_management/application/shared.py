import traceback
from ddd.order_management.application import dtos

def handle_invalid_order_operation(err):
    #TODO handle logger
    #logger.error(f"{err}")
    response_dto = dtos.ResponseDTO(
        success=False,
        message=str(err)
    )
    return response_dto

def handle_unexpected_error(err_details):
    #TODO log err details but dont return in results
    #logger.error(f"{err_details}", exc_info=True)
    print(traceback.print_exc())
    response_dto = dtos.ResponseDTO(
        success=False,
        message="An unexpected error occured. Please contact support."
    )
    return response_dto