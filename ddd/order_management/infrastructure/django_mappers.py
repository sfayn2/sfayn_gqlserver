import ast
from typing import List
from ddd.order_management.domain import value_objects, models
from ddd.order_management.application import dtos, mappers
from vendor_management import models as django_vendor_models

class CouponMapper:

    @staticmethod
    def to_domain(coupon_code) -> dtos.CouponDTO:
        #only care on coupon code & load the rest of attrs value from db
        django_coupon = django_vendor_models.Coupon.objects.filter(coupon_code=coupon_code).values().first()
        return dtos.CouponDTO(**django_coupon)

class LineItemMapper:

    @staticmethod
    def to_django(order_id, line_item: models.LineItem) -> dict:
        return {
                "product_sku": line_item.product_sku,
                "order_id": order_id,
                "defaults":  {
                    'product_name': line_item.product_name, 
                    'vendor_name': line_item.vendor.name, 
                    'vendor_country': line_item.vendor.country, 
                    'product_category': line_item.product_category, 
                    'options': line_item.options, 
                    'product_price': line_item.product_price.amount, 
                    'product_currency': line_item.product_price.currency,
                    'order_quantity': line_item.order_quantity, 
                    'package_weight': line_item.package.weight,
                    'package_length': line_item.package.dimensions[0],
                    'package_width': line_item.package.dimensions[1],
                    'package_height': line_item.package.dimensions[2],
                    'is_free_gift': line_item.is_free_gift, 
                    'is_taxable': line_item.is_taxable
                }
            }

    def to_domain(django_line_item) -> models.LineItem:
        return models.LineItem(
            product_sku=django_line_item.product_sku,
            product_name=django_line_item.product_name,
            vendor=value_objects.VendorDetails(
                name=django_line_item.vendor_name,
                country=django_line_item.vendor_country
            ),
            product_category=django_line_item.product_category,
            options=ast.literal_eval(django_line_item.options),
            product_price=value_objects.Money(
                amount=django_line_item.product_price,
                currency=django_line_item.product_currency
            ),
            order_quantity=django_line_item.order_quantity,
            package=value_objects.Package(
                weight=django_line_item.package_weight,
                dimensions=[django_line_item.package_length, django_line_item.package_width, django_line_item.package_height] 
            ),
            is_free_gift=django_line_item.is_free_gift,
            is_taxable=django_line_item.is_taxable
        )


class OrderMapper:

    @staticmethod
    def to_django(order_dto: dtos.OrderDTO):
        return {
            'order_id': order_dto.order_id,
            'defaults': {
                    'date_created': order_dto.date_created,
                    'delivery_street': order_dto.destination.street,
                    'delivery_city': order_dto.destination.city,
                    'delivery_postal': order_dto.destination.postal,
                    'delivery_country': order_dto.destination.country, 
                    'delivery_state': order_dto.destination.state, 
                    'customer_first_name': order_dto.customer_details.first_name, 
                    'customer_last_name': order_dto.customer_details.last_name, 
                    'customer_email': order_dto.customer_details.email if order_dto.customer_details else None, 
                    'shipping_method': order_dto.shipping_details.method.value if order_dto.shipping_details else None, 
                    'shipping_delivery_time': order_dto.shipping_details.delivery_time if order_dto.shipping_details else None,
                    'shipping_cost': order_dto.shipping_details.cost.amount if order_dto.shipping_details else None,
                    'shipping_tracking_reference': order_dto.shipping_reference,
                    'payment_method': order_dto.payment_details.method.value if order_dto.payment_details else None,
                    'payment_reference': order_dto.payment_details.transaction_id if order_dto.payment_details else None,
                    'payment_amount': order_dto.payment_details.paid_amount.amount if order_dto.payment_details else None, 
                    'cancellation_reason': order_dto.cancellation_reason, 
                    'total_discounts_fee': order_dto.total_discounts_fee.amount if order_dto.total_discounts_fee else None, 
                    'offer_details': order_dto.offer_details if order_dto.offer_details else [],
                    'tax_details': order_dto.tax_details if order_dto.tax_details else [], 
                    'tax_amount': order_dto.tax_amount.amount if order_dto.tax_amount else None, 
                    'total_amount': order_dto.total_amount.amount if order_dto.total_amount else None, 
                    'final_amount': order_dto.final_amount.amount if order_dto.final_amount else None, 
                    'shipping_tracking_reference': order_dto.shipping_reference, 
                    'coupons': [coupon.coupon_code for coupon in order_dto.coupons], 
                    'order_status': order_dto.order_status.value, 
                    'currency': order_dto.currency,
                    'date_modified': order_dto.date_modified
                }
        }

    @staticmethod
    def to_domain(django_order_object) -> models.Order:
        shipping_details = None
        if django_order_object.shipping_method:
            shipping_details=value_objects.ShippingDetails(
                method=django_order_object.shipping_method,
                delivery_time=django_order_object.shipping_delivery_time,
                cost=value_objects.Money(
                    amount=django_order_object.shipping_cost,
                    currency=django_order_object.currency
                )
            )

        payment_details = None
        if django_order_object.payment_method:
            payment_details=value_objects.PaymentDetails(
                method=django_order_object.payment_method,
                transaction_id=django_order_object.payment_reference,
                paid_amount=dtos.MoneyDTO(
                    amount=django_order_object.payment_amount,
                    currency=django_order_object.currency
                )
            )

        return models.Order(
            order_id=django_order_object.order_id,
            date_created=django_order_object.date_created,
            date_modified=django_order_object.date_modified, 
            destination=value_objects.Address(
                street=django_order_object.delivery_street,
                city=django_order_object.delivery_city,
                postal=django_order_object.delivery_postal,
                country=django_order_object.delivery_country,
                state=django_order_object.delivery_state
            ),
            line_items=[
                LineItemMapper.to_domain(item) for item in django_order_object.line_items.all()
            ],
            customer_details=value_objects.CustomerDetails(
                first_name=django_order_object.customer_first_name,
                last_name=django_order_object.customer_last_name,
                email=django_order_object.customer_email
            ),
            shipping_details=shipping_details if shipping_details else None,
            payment_details=payment_details if payment_details else None,
            cancellation_reason=django_order_object.cancellation_reason,
            total_discounts_fee=value_objects.Money(
                amount=django_order_object.total_discounts_fee,
                currency=django_order_object.currency
            ),
            offer_details=ast.literal_eval(django_order_object.offer_details) if django_order_object.offer_details else None,
            tax_details=ast.literal_eval(django_order_object.tax_details) if django_order_object.tax_details else None,
            tax_amount=value_objects.Money(
                amount=django_order_object.tax_amount,
                currency=django_order_object.currency
            ),
            total_amount=value_objects.Money(
                amount=django_order_object.total_amount,
                currency=django_order_object.currency
            ),
            final_amount=value_objects.Money(
                amount=django_order_object.final_amount,
                currency=django_order_object.currency
            ),
            shipping_reference=django_order_object.shipping_tracking_reference,
            coupons=[CouponMapper.to_domain(item) for item in ast.literal_eval(django_order_object.coupons)],
            currency=django_order_object.currency,
            order_status=django_order_object.order_status
        )

class OfferStrategyMapper:

    @staticmethod
    def to_domain(django_filter_results) -> value_objects.OfferStrategy:
        #first coupon is invalid and second is valid should not stop processing Offer, hence, skipping error
        coupons = []
        for item in django_filter_results.coupons:
            try:
                coupons.append(value_objects.Coupon(**item))
            except:
                #TODO: add logger
                continue
        
        conditions = django_filter_results.conditions
        django_filter_results.pop("coupons")
        django_filter_results.pop("conditions")

        return value_objects.OfferStrategy(
            **django_filter_results,
            conditions=ast.literal_eval(conditions),
            coupons=coupons
        )


class ShippingOptionStrategyMapper:

    @staticmethod
    def to_domain(django_filter_results) -> value_objects.ShippingOptionStrategy:
        return value_objects.ShippingOptionStrategy(
            name=django_filter_results.get("name"),
            delivery_time=django_filter_results.get("delivery_time"),
            conditions=django_filter_results.get("conditions"),
            base_cost=value_objects.Money(django_filter_results.get("base_cost")),
            flat_rate=value_objects.Money(django_filter_results.get("flat_rate")),
            currency=django_filter_results.get("currency"),
            is_active=django_filter_results.get("is_active")
        )
