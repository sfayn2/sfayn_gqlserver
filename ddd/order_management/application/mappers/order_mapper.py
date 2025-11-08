import ast
from typing import List
from dataclasses import asdict
from ddd.order_management.application import dtos, mappers
from ddd.order_management.domain import models, value_objects

class OrderMapper:

    @staticmethod
    def to_dto(order: models.Order) -> dtos.OrderDTO:
        response_dto = dtos.OrderDTO(
            tenant_id=order.tenant_id,
            customer_details=dtos.CustomerDetailsDTO(
                **asdict(order.customer_details)

            ),
            order_id=order.order_id,
            currency=order.currency,
            order_status=order.order_status,
            payment_status=order.payment_status,
            line_items=[dtos.LineItemDTO(
                **asdict(line_item)
            ) for line_item in order.line_items],
            shipments=[dtos.ShipmentItemDTO(**asdict(item)) for item in order.shipments],
            date_created=order.date_created,
            date_modified=order.date_modified
        )

        return response_dto
