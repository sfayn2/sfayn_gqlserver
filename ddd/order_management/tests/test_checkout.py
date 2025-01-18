import uuid
from datetime import datetime
from ddd.order_management.application import message_bus, unit_of_work, dtos
from ddd.order_management.application import commands
from ddd.order_management.domain import enums, value_objects, models

def test_checkout():
    uow = unit_of_work.DjangoUnitOfWork()
    #request_dto = dtos.CheckoutRequestDTO.parse_raw(request.body)
    raw_json_data = """
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "JohnDoe@gmail.com",
            "address": {
                "street": "123 main street",
                "city": "new York",
                "postal_code": "1001"
            },
            "line_items": [
                {"product_sku": "sku-1", "order_quantity":1, "price": { "amount": 1.12, "currency": "SGD"} },
                {"product_sku": "sku-2", "order_quantity":1, "price": { "amount": 1.12, "currency": "SGD"} }
            ]
        }
"""
    request_dto = dtos.CheckoutRequestDTO.parse_raw(raw_json_data)
    command = commands.CheckoutCommand(
        first_name=request_dto.first_name,
        last_name=request_dto.last_name,
        email=request_dto.email,
        address=request_dto.address,
        line_items=request_dto.line_items
    )

    order = message_bus.handle(command, uow)

    response_dto = dtos.CheckoutResponseDTO(
        order_id=order.id,
        status=order.status,
        message="Order successfully created."
    )

    print(response_dto.dict())