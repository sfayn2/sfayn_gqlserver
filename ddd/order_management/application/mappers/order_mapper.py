import ast
from typing import List
from dataclasses import asdict
from ddd.order_management.application import dtos
from ddd.order_management.domain import models, value_objects
from ddd.order_management.application.mappers.line_item_mapper import LineItemMapper
from ddd.order_management.application.mappers.address_mapper import AddressMapper
from ddd.order_management.application.mappers.customer_details_mapper import CustomerDetailsMapper
from ddd.order_management.application.mappers.shipping_details_mapper import ShippingDetailsMapper
from ddd.order_management.application.mappers.payment_details_mapper import PaymentDetailsMapper
from ddd.order_management.application.mappers.money_mapper import MoneyMapper
from ddd.order_management.application.mappers.coupon_mapper import CouponMapper

class OrderMapper:
    @staticmethod
    def to_domain(order_dto: dtos.OrderDTO) -> models.Order:
        line_items = [LineItemMapper.to_domain(item) for item in order_dto.line_items]
        return models.Order(
            order_id=order_dto.order_id,
            date_created=order_dto.date_created,
            destination=AddressMapper.to_domain(order_dto.destination),
            line_items=line_items,
            customer_details=CustomerDetailsMapper.to_domain(order_dto.customer_details),
            shipping_details=ShippingDetailsMapper.to_domain(order_dto.shipping_details) if order_dto.shipping_details else None,
            payment_details=PaymentDetailsMapper.to_domain(order_dto.payment_details) if order_dto.payment_details else None,
            cancellation_reason=order_dto.cancellation_reason,
            total_discounts_fee=MoneyMapper.to_domain(order_dto.total_discounts_fee),
            offer_details=order_dto.offer_details,
            tax_details=order_dto.tax_details,
            tax_amount=MoneyMapper.to_domain(order_dto.tax_amount),
            total_amount=MoneyMapper.to_domain(order_dto.total_amount),
            final_amount=MoneyMapper.to_domain(order_dto.final_amount),
            shipping_reference=order_dto.shipping_reference,
            coupons=[CouponMapper.to_domain(coupon) for coupon in order_dto.coupons], 
            order_status=order_dto.order_status,
            date_modified=order_dto.date_modified
        )
