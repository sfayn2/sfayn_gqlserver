import ast, json
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
                    'payment_method': order.payment_details.method if order.payment_details else None,
                    'payment_reference': order.payment_details.transaction_id if order.payment_details else None,
                    'payment_amount': order.payment_details.paid_amount.amount if order.payment_details else None, 
                    'cancellation_reason': order.cancellation_reason, 
                    'total_discounts_fee': order.total_discounts_fee.amount if order.total_discounts_fee else None, 
                    'offer_details': json.dumps([offd for offd in order.offer_details]),
                    'tax_details': json.dumps([taxd for taxd in order.tax_details]),
                    'tax_amount': order.tax_amount.amount if order.tax_amount else None, 
                    'total_amount': order.total_amount.amount if order.total_amount else None, 
                    'final_amount': order.final_amount.amount if order.final_amount else None, 
                    'shipping_tracking_reference': order.shipping_reference, 
                    'coupons': json.dumps([coupon.coupon_code for coupon in order.coupons]), 
                    'order_stage': order.order_stage.value, 
                    'activity_status': order.activity_status, 
                    'currency': order.currency,
                    'tenant_id': order.tenant_id,
                    'date_modified': order.date_modified
                }
        }

    @staticmethod
    def to_domain(django_order_object) -> models.Order:

        #for item in django_order_object.line_items.all():
        #    if item.vendor_id:
        #        vendor_details = value_objects.VendorDetails(
        #            vendor_id=item.vendor_id,
        #            name=item.vendor_name,
        #            country=item.vendor_country
        #        )
        #        break

        #TODO: what if all items has been remove for specific order?
        vendor_id = django_order_object.line_items.all().values_list("vendor_id", flat=True)[0]

        django_coupons = []
        for item in json.loads(django_order_object.coupons):
            vendor_coupon_snapshot = django_snapshots.VendorCouponSnapshot.objects.filter(coupon_code=item, vendor_id=vendor_id)
            if vendor_coupon_snapshot.exists():
                django_coupons.append(django_mappers.CouponMapper.to_domain(vendor_coupon_snapshot))


        return models.Order(
            order_id=django_order_object.order_id,
            tenant_id=django_order_object.tenant_id,
            date_created=django_order_object.date_created,
            date_modified=django_order_object.date_modified, 
            destination=django_mappers.AddressMapper.to_domain(django_order_object),
            line_items=[
                django_mappers.LineItemMapper.to_domain(item) for item in django_order_object.line_items.all()
            ],
            activities=[
                django_mappers.OtherActivityMapper.to_domain(item) for item in django_order_object.other_activities.all()
            ],
            customer_details=django_mappers.CustomerDetailsMapper.to_domain(django_order_object),
            shipping_details=django_mappers.ShippingDetailsMapper.to_domain(django_order_object) if django_order_object.shipping_method else None,
            payment_details=django_mappers.PaymentDetailsMapper.to_domain(django_order_object) if django_order_object.payment_method else None,
            cancellation_reason=django_order_object.cancellation_reason,
            total_discounts_fee=value_objects.Money(
                amount=django_order_object.total_discounts_fee,
                currency=django_order_object.currency
            ),
            offer_details=json.loads(django_order_object.offer_details) if django_order_object.offer_details else None,
            tax_details=json.loads(django_order_object.tax_details) if django_order_object.tax_details else None,
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
            order_stage=enums.OrderStage(django_order_object.order_stage),
            activity_status=django_order_object.activity_status
        )

