import ast
from ddd.order_management.domain import value_objects, models, enums
from ddd.order_management.infrastructure import django_mappers
from order_management import models as django_snapshots

class OrderMapper:

    @staticmethod
    def to_django(order: models.Order):
        return {
            'order_id': order.order_id,
            'defaults': {
                    'date_created': order.date_created,
                    'delivery_street': order.destination.street,
                    'delivery_city': order.destination.city,
                    'delivery_postal': order.destination.postal,
                    'delivery_country': order.destination.country, 
                    'delivery_state': order.destination.state, 
                    'customer_first_name': order.customer_details.first_name, 
                    'customer_last_name': order.customer_details.last_name, 
                    'customer_email': order.customer_details.email if order.customer_details else None, 
                    'shipping_method': order.shipping_details.method.value if order.shipping_details else None, 
                    'shipping_delivery_time': order.shipping_details.delivery_time if order.shipping_details else None,
                    'shipping_cost': order.shipping_details.cost.amount if order.shipping_details else None,
                    'shipping_tracking_reference': order.shipping_reference,
                    'payment_method': order.payment_details.method.value if order.payment_details else None,
                    'payment_reference': order.payment_details.transaction_id if order.payment_details else None,
                    'payment_amount': order.payment_details.paid_amount.amount if order.payment_details else None, 
                    'cancellation_reason': order.cancellation_reason, 
                    'total_discounts_fee': order.total_discounts_fee.amount if order.total_discounts_fee else None, 
                    'offer_details': order.offer_details if order.offer_details else [],
                    'tax_details': order.tax_details if order.tax_details else [], 
                    'tax_amount': order.tax_amount.amount if order.tax_amount else None, 
                    'total_amount': order.total_amount.amount if order.total_amount else None, 
                    'final_amount': order.final_amount.amount if order.final_amount else None, 
                    'shipping_tracking_reference': order.shipping_reference, 
                    'coupons': [coupon.coupon_code for coupon in order.coupons], 
                    'order_status': order.order_status.value, 
                    'currency': order.currency,
                    'date_modified': order.date_modified
                }
        }

    @staticmethod
    def to_domain(django_order_object) -> models.Order:
        shipping_details = None
        if django_order_object.shipping_method:
            shipping_details=value_objects.ShippingDetails(
                method=enums.ShippingMethod(django_order_object.shipping_method),
                delivery_time=django_order_object.shipping_delivery_time,
                cost=value_objects.Money(
                    amount=django_order_object.shipping_cost,
                    currency=django_order_object.currency
                )
            )

        for item in django_order_object.line_items.all():
            if item.vendor:
                vendor_details = item.vendor
                break

        django_coupons = []
        for item in ast.literal_eval(django_order_object.coupons):
            vendor_coupon_snapshot = django_snapshots.VendorCouponSnapshot.objects.filter(coupon_code=item, vendor_offer_snapshot__vendor__id=vendor_details.id)
            if vendor_coupon_snapshot.exists():
                django_coupons.append(django_mappers.CouponMapper.to_domain(vendor_coupon_snapshot))

        payment_details = None
        if django_order_object.payment_method:
            payment_details=value_objects.PaymentDetails(
                method=django_order_object.payment_method,
                transaction_id=django_order_object.payment_reference,
                paid_amount=value_objects.Money(
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
                postal=int(django_order_object.delivery_postal),
                country=django_order_object.delivery_country,
                state=django_order_object.delivery_state
            ),
            line_items=[
                django_mappers.LineItemMapper.to_domain(item) for item in django_order_object.line_items.all()
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
            coupons=django_coupons,
            order_status=enums.OrderStatus(django_order_object.order_status)
        )

