import uuid
import os
from ddd.order_management.infrastructure.adapters import unit_of_work
import pytest
import json
from datetime import datetime
from unittest import mock
from decimal import Decimal

from ddd.order_management.application import message_bus, dtos
from ddd.order_management.application import commands
from ddd.order_management.domain import enums, value_objects, models

@pytest.fixture
def mock_uow():
    return mock.MagicMock(unit_of_work.DjangoUnitOfWork())

@pytest.fixture
def mock_order():
    return models.Order.create_draft_order(
        destination=value_objects.Address(
            street="123 main street",
            city="New York",
            postal=1001,
            state="NYC",
            country="USA"
        ),
        customer_details=value_objects.CustomerDetails(
            first_name="John",
            last_name="Doe",
            email="JohnDoe@gmail.com"
        ),
        line_items=[models.LineItem(
                product_sku="Sku-1",
                product_name="Product 1",
                vendor_name="Vendor 1",
                product_category="Category 1",
                options={"COLOR":"RED"},
                product_price=value_objects.Money(
                    amount=Decimal("2.1"),
                    currency="SGD"
                ),
                order_quantity=1,
                package=value_objects.Package(
                    weight=Decimal("1.5"),
                    dimensions=(10,10,10)
                )
        )]

    )

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sfayn_gqlserver.settings")

#@pytest.mark.django_db
def test_checkout(mock_uow, mock_order):


    mock_uow.order.save = mock.MagicMock()
    mock_uow.commit = mock.MagicMock()

    with mock.patch("ddd.order_management.application.message_bus.handle", return_value=mock_order):
        dict_data =  {
                "customer_details": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "JohnDoe@gmail.com"
                },
                "address": {
                    "street": "123 main street",
                    "city": "New York",
                    "state": "NYC",
                    "postal": "1001",
                    "country": "USA"
                },
                "line_items": [
                    {"product_sku": "sku-1", "product_name": "Product 1", 
                     "vendor_name": "Vendor 1", "product_category": "Category 1", 
                     "order_quantity":1, "options": {"COLOR":"RED"},  
                     "product_price": { "amount": 2.1, "currency": "SGD"}, 
                     "package": { "weight": 1.5, "dimensions": (10, 10, 10) } },
                ]
            }


    request_dto = dtos.CheckoutRequestDTO.model_validate(dict_data)
    command = commands.CheckoutCommand(
        customer_details=request_dto.customer_details,
        address=request_dto.address,
        line_items=request_dto.line_items
    )

    order = message_bus.handle(command, mock_uow)

    response_dto = dtos.CheckoutResponseDTO(
        order_id=order.order_id,
        order_status=order.order_status,
        message="Order successfully created."
    )

    #assert order is mock_order
    assert response_dto.order_status == order.order_status
    assert response_dto.message == "Order successfully created."

    #mock_uow.order.save.assert_called_once_with(mock_order)
    mock_uow.order.save.assert_called_once()
    mock_uow.commit.assert_called_once()
