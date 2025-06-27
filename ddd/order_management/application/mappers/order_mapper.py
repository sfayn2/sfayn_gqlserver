import ast
from typing import List
from dataclasses import asdict
from ddd.order_management.application import dtos, mappers
from ddd.order_management.domain import models, value_objects

class OrderMapper:

    @staticmethod
    def to_dto(order: models.Order) -> dtos.OrderDTO:
        response_dto = dtos.OrderDTO(
                order_id=order.order_id,
                date_created=order.date_created,
                destination=asdict(order.destination),
                line_items=[asdict(item) for item in order.line_items],
                customer_details=asdict(order.customer_details) if order.customer_details else None,
                shipping_details=asdict(order.shipping_details) if order.shipping_details else None,
                payment_details=asdict(order.payment_details) if order.payment_details else None,
                cancellation_reason=order.cancellation_reason,
                total_discounts_fee=asdict(order.total_discounts_fee),
                offer_details=order.offer_details,
                tax_details=order.tax_details,
                tax_amount=asdict(order.tax_amount),
                total_amount=asdict(order.total_amount),
                final_amount=asdict(order.final_amount),
                shipping_reference=order.shipping_reference,
                coupons=asdict(order.coupons) if order.coupons else None,
                order_status=order.order_status,
                currency=order.currency,
                date_modified=order.date_modified)

        return response_dto
