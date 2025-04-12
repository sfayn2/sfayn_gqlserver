import ast
from ddd.order_management.application import dtos
from vendor_management import models as django_vendor_models

class CouponMapper:
    @staticmethod
    def from_django_filter(coupon_code) -> dtos.CouponDTO:
        #only care on coupon code & load the rest of attrs value from db
        django_coupon = django_vendor_models.Coupon.objects.filter(coupon_code=coupon_code).values().first()
        return dtos.CouponDTO(**django_coupon)

class LineItemMapper:
    @staticmethod
    def from_django_model(django_line_item) -> dtos.LineItemDTO:
        return dtos.LineItemDTO(
            product_sku=django_line_item.product_sku,
            product_name=django_line_item.product_name,
            vendor=dtos.VendorDetailsDTO(
                name=django_line_item.vendor_name,
                country=django_line_item.vendor_country
            ),
            product_category=django_line_item.product_category,
            options=ast.literal_eval(django_line_item.options),
            product_price=dtos.MoneyDTO(
                amount=django_line_item.product_price,
                currency=django_line_item.product_currency
            ),
            order_quantity=django_line_item.order_quantity,
            package=dtos.PackageDTO(
                weight=django_line_item.package_weight,
                dimensions=[django_line_item.package_length, django_line_item.package_width, django_line_item.package_height] 
            ),
            is_free_gift=django_line_item.is_free_gift,
            is_taxable=django_line_item.is_taxable
        )

    @staticmethod
    def to_django(order_id, line_item_dto: dtos.LineItemDTO) -> dict:
        return {
                "product_sku": line_item_dto.product_sku,
                "order_id": order_id,
                "defaults":  {
                    'product_name': line_item_dto.product_name, 
                    'vendor_name': line_item_dto.vendor.name, 
                    'vendor_country': line_item_dto.vendor.country, 
                    'product_category': line_item_dto.product_category, 
                    'options': line_item_dto.options, 
                    'product_price': line_item_dto.product_price.amount, 
                    'product_currency': line_item_dto.product_price.currency,
                    'order_quantity': line_item_dto.order_quantity, 
                    'package_weight': line_item_dto.package.weight,
                    'package_length': line_item_dto.package.dimensions[0],
                    'package_width': line_item_dto.package.dimensions[1],
                    'package_height': line_item_dto.package.dimensions[2],
                    'is_free_gift': line_item_dto.is_free_gift, 
                    'is_taxable': line_item_dto.is_taxable
                }
            }


class OrderMapper:
    @staticmethod
    def from_django_model(django_order) -> dtos.OrderDTO:
        shipping_details_dto = None
        if django_order.shipping_method:
            shipping_details_dto=dtos.ShippingDetailsDTO(
                method=django_order.shipping_method,
                delivery_time=django_order.shipping_delivery_time,
                cost=dtos.MoneyDTO(
                    amount=django_order.shipping_cost,
                    currency=django_order.currency
                )
            )

        payment_details_dto = None
        if django_order.payment_method:
            payment_details_dto=dtos.PaymentDetailsDTO(
                method=django_order.payment_method,
                transaction_id=django_order.payment_reference,
                paid_amount=dtos.MoneyDTO(
                    amount=django_order.payment_amount,
                    currency=django_order.currency
                )
            )

        return dtos.OrderDTO(
            order_id=django_order.order_id,
            date_created=django_order.date_created,
            date_modified=django_order.date_modified, 
            destination=dtos.AddressDTO(
                street=django_order.delivery_street,
                city=django_order.delivery_city,
                postal=django_order.delivery_postal,
                country=django_order.delivery_country,
                state=django_order.delivery_state
            ),
            line_items=[
                LineItemMapper.from_django_model(item) for item in django_order.line_items.all()
            ],
            customer_details=dtos.CustomerDetailsDTO(
                first_name=django_order.customer_first_name,
                last_name=django_order.customer_last_name,
                email=django_order.customer_email
            ),
            shipping_details=shipping_details_dto if shipping_details_dto else None,
            payment_details=payment_details_dto if payment_details_dto else None,
            cancellation_reason=django_order.cancellation_reason,
            total_discounts_fee=dtos.MoneyDTO(
                amount=django_order.total_discounts_fee,
                currency=django_order.currency
            ),
            offer_details=ast.literal_eval(django_order.offer_details) if django_order.offer_details else None,
            tax_details=ast.literal_eval(django_order.tax_details) if django_order.tax_details else None,
            tax_amount=dtos.MoneyDTO(
                amount=django_order.tax_amount,
                currency=django_order.currency
            ),
            total_amount=dtos.MoneyDTO(
                amount=django_order.total_amount,
                currency=django_order.currency
            ),
            final_amount=dtos.MoneyDTO(
                amount=django_order.final_amount,
                currency=django_order.currency
            ),
            shipping_reference=django_order.shipping_tracking_reference,
            coupons=[CouponMapper.from_django_filter(item) for item in ast.literal_eval(django_order.coupons)],
            currency=django_order.currency,
            order_status=django_order.order_status
        )

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