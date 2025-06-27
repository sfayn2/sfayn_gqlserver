import ast
from typing import List
from dataclasses import asdict
from ddd.order_management.application import dtos, mappers
from ddd.order_management.domain import models, value_objects

class OrderMapper:
    #@staticmethod
    #def to_domain(order_dto: dtos.OrderDTO) -> models.Order:
    #    line_items = [mappers.LineItemMapper.to_domain(item) for item in order_dto.line_items]
    #    return models.Order(
    #        order_id=order_dto.order_id,
    #        date_created=order_dto.date_created,
    #        destination=mappers.AddressMapper.to_domain(order_dto.destination),
    #        line_items=line_items,
    #        customer_details=mappers.CustomerDetailsMapper.to_domain(order_dto.customer_details),
    #        shipping_details=mappers.ShippingDetailsMapper.to_domain(order_dto.shipping_details) if order_dto.shipping_details else None,
    #        payment_details=mappers.PaymentDetailsMapper.to_domain(order_dto.payment_details) if order_dto.payment_details else None,
    #        cancellation_reason=order_dto.cancellation_reason,
    #        total_discounts_fee=mappers.MoneyMapper.to_domain(order_dto.total_discounts_fee),
    #        offer_details=order_dto.offer_details,
    #        tax_details=order_dto.tax_details,
    #        tax_amount=mappers.MoneyMapper.to_domain(order_dto.tax_amount),
    #        total_amount=mappers.MoneyMapper.to_domain(order_dto.total_amount),
    #        final_amount=mappers.MoneyMapper.to_domain(order_dto.final_amount),
    #        shipping_reference=order_dto.shipping_reference,
    #        coupons=[mappers.CouponMapper.to_domain(coupon) for coupon in order_dto.coupons], 
    #        order_status=order_dto.order_status,
    #        date_modified=order_dto.date_modified
    #    )

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
