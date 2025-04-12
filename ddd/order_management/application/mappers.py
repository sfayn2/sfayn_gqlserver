import ast
from typing import List
from dataclasses import asdict
from ddd.order_management.application import dtos
from ddd.order_management.domain import models, value_objects

class OrderResponseMapper:

    @staticmethod
    def to_dto(order: models.Order, success: bool = True, message: str = None) -> dtos.OrderResponseDTO:
        response_dto = dtos.OrderResponseDTO(
                order_id=order.order_id,
                order_status=order.order_status,
                success=success,
                message=message,
                tax_details=order.tax_details,
                offer_details=order.offer_details,
                shipping_details=asdict(order.shipping_details),
                tax_amount=asdict(order.tax_amount),
                total_discounts_fee=asdict(order.total_discounts_fee),
                final_amount=asdict(order.final_amount)
            )
        return response_dto

class ShippingDetailsMapper:

    @staticmethod
    def from_domain(shipping_details: value_objects.ShippingDetails) -> dtos.ShippingDetailsDTO:
        return dtos.ShippingDetailsDTO(**asdict(shipping_details))

    @staticmethod
    def to_domain(shipping_details_dto: dtos.ShippingDetailsDTO) -> value_objects.ShippingDetails:
        return value_objects.ShippingDetails(
            method=shipping_details_dto.method,
            delivery_time=shipping_details_dto.delivery_time,
            cost=value_objects.Money(
                amount=shipping_details_dto.cost.amount,
                currency=shipping_details_dto.cost.currency
            )
        )



class ShippingOptionsResponseMapper:

    @staticmethod
    def to_dtos(shipping_options: List[value_objects.ShippingDetails]) -> List[dtos.ShippingDetailsDTO]:
        return [ShippingDetailsMapper.from_domain(option) for option in shipping_options]

class VendorDetailsMapper:
    @staticmethod
    def to_domain(vendor_details_dto: dtos.VendorDetailsDTO) -> value_objects.VendorDetails:
        return value_objects.VendorDetails(**vendor_details_dto.model_dump())

class MoneyMapper:
    @staticmethod
    def to_domain(money_dto: dtos.MoneyDTO) -> value_objects.Money:
        return value_objects.Money(**money_dto.model_dump())

class CouponMapper:
    @staticmethod
    def to_domain(coupon_dto: dtos.CouponDTO) -> value_objects.Coupon:
        return value_objects.Coupon(**coupon_dto.model_dump())

class PackageMapper:

    @staticmethod
    def to_domain(package_dto: dtos.PackageDTO) -> value_objects.Package:
        return value_objects.Package(**package_dto.model_dump())

class AddressMapper:
    @staticmethod
    def to_domain(address_dto: dtos.AddressDTO) -> value_objects.Address:
        return value_objects.Address(**address_dto.model_dump())

class CustomerDetailsMapper:

    @staticmethod
    def to_domain(custom_details_dto: dtos.CustomerDetailsDTO) -> value_objects.CustomerDetails:
        return value_objects.CustomerDetails(**custom_details_dto.model_dump())

class PaymentDetailsMapper:

    @staticmethod
    def to_domain(payment_details_dto: dtos.PaymentDetailsDTO) -> value_objects.PaymentDetails:
        return value_objects.PaymentDetails(
            order_id=payment_details_dto.order_id,
            method=payment_details_dto.method,
            paid_amount=value_objects.Money(
                amount=payment_details_dto.paid_amount.amount,
                currency=payment_details_dto.paid_amount.currency
            ),
            transaction_id=payment_details_dto.transaction_id,
            status=payment_details_dto.status
        )


class LineItemMapper:
    @staticmethod
    def to_domain(line_item_dto: dtos.LineItemDTO) -> models.LineItem:
        return models.LineItem(
            product_sku=line_item_dto.product_sku,
            product_name=line_item_dto.product_name,
            vendor=VendorDetailsMapper.to_domain(line_item_dto.vendor),
            product_category=line_item_dto.product_category,
            options=line_item_dto.options,
            product_price=MoneyMapper.to_domain(line_item_dto.product_price),
            order_quantity=line_item_dto.order_quantity,
            package=PackageMapper.to_domain(line_item_dto.package),
            is_free_gift=line_item_dto.is_free_gift,
            is_taxable=line_item_dto.is_taxable
        )


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
            payment_details=PaymentDetailsMapper.to_domain(order_dto.payment_details) if self.payment_details else None,
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
