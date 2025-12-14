import ast
from typing import List
from dataclasses import asdict
from ddd.order_management.application import dtos, mappers
from ddd.order_management.domain import models, value_objects

class OrderMapper:

    @staticmethod
    def to_response_dto(order: models.Order) -> dtos.OrderResponseDTO:
        response_dto = dtos.OrderResponseDTO(
            order_id=order.order_id,
            line_items=[
                mappers.LineItemMapper.to_response_dto(item)
                for item in order.line_items
            ],
            shipments=[
                mappers.ShipmentMapper.to_response_dto(item) 
                for item in order.shipments
            ],
            customer_details=mappers.CustomerDetailsMapper.to_response_dto(order.customer_details),
            currency=order.currency,
            tenant_id=order.tenant_id,
            order_status=order.order_status,
            payment_status=order.payment_status,
            date_created=order.date_created,
            date_modified=order.date_modified
        )

        return response_dto
