import pytest
from datetime import datetime
from unittest import mock
from decimal import Decimal
from ddd.order_management.infrastructure import dtos
from ddd.order_management.domain import models, value_objects, enums

@pytest.fixture
def mock_django_line_item():
    m = mock.MagicMock()
    m.product_sku = "SKU123"
    m.product_name = "Test Product"
    m.vendor_name = "VENDOR1"
    m.product_category = "Category1"
    m.options = '{"color": "red", "size": "m" }'
    m.product_price = Decimal("50.00")
    m.currency = "SGD"
    m.order_quantity = 2
    m.weight = Decimal("1.5")
    m.length = 10
    m.width = 5
    m.height = 5
    m.is_free_gift = False
    m.is_taxable = True
    return m

@pytest.fixture
def domain_line_item():
    return models.LineItem(
        product_sku="SKU123",
        product_name="Test Product",
        vendor_name="VENDOR1",
        product_category="Category1",
        options = {"color": "red", "size": "m" },
        product_price=value_objects.Money(
            amount=Decimal("50.00"),
            currency="SGD"
        ),
        order_quantity=2,
        package=value_objects.Package(
            weight=Decimal("1.5"),
            dimensions=(10, 5, 5)
        ),
        is_free_gift=False,
        is_taxable=True
    )

@pytest.fixture
def mock_django_order(mock_django_line_item):
    m = mock.MagicMock()
    m.order_id = "ORDER123"
    m.date_created = datetime(2025, 1, 1, 12, 0, 0)
    m.date_modified = datetime(2025, 1, 2, 12, 0, 0)
    m.delivery_street = "123 Main St"
    m.delivery_city = "New York"
    m.delivery_postal = 10001
    m.delivery_state = "NY"
    m.delivery_country = "USA"
    m.customer_first_name = "John"
    m.customer_last_name = "Doe"
    m.customer_email = "john.doe@example.com"
    m.shipping_method = enums.ShippingMethod.STANDARD.value
    m.shipping_delivery_time = "3-5 business days"
    m.shipping_cost = Decimal("10.00")
    m.currency = "SGD"
    m.payment_method = enums.PaymentMethod.PAYPAL.value
    m.payment_reference = "PAY123"
    m.payment_amount = Decimal("110.50")
    m.cancellation_reason = ""
    m.total_discounts_fee = Decimal("5.00")
    m.offer_details = "New Year Offer"
    m.tax_details = "Tax Included"
    m.tax_amount = Decimal("15.00")
    m.total_amount = Decimal("120.00")
    m.final_amount = Decimal("110.50")
    m.shipping_tracking_reference = "TRACK123"
    m.coupon_codes = ["NEWYEAR2025"]
    m.status = enums.OrderStatus.PENDING.value
    m.line_items.all.return_value = [mock_django_line_item]
    return m

@pytest.fixture
def domain_order(domain_line_item):
    return models.Order(
        order_id="ORDER123",
        date_created = datetime(2025, 1, 1, 12, 0, 0),
        date_modified = datetime(2025, 1, 2, 12, 0, 0),
        destination=value_objects.Address(
            street="123 Main St",
            city="New York",
            postal=10001,
            country="USA",
            state="NY"
        ),
        line_items=[domain_line_item],
        customer_details=value_objects.CustomerDetails(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        ),
        shipping_details=value_objects.ShippingDetails(
            method=enums.ShippingMethod.STANDARD.value,
            delivery_time="3-5 business days",
            cost=value_objects.Money(
                amount=Decimal("10.00"),
                currency="SGD"    
            ),
            orig_cost=value_objects.Money(
                amount=Decimal("10.00"),
                currency="SGD"    
            )
        ),
        payment_details=value_objects.PaymentDetails(
            method=enums.PaymentMethod.PAYPAL,
            transaction_id="PAY123",
            paid_amount=value_objects.Money(
                amount=Decimal("110.50"),
                currency="SGD"
            )
        ),
        cancellation_reason="",
        total_discounts_fee=value_objects.Money(
            amount=Decimal("5.00"),
            currency="SGD"
        ),
        offer_details="New Year Offer",
        tax_details="Tax Included",
        tax_amount=value_objects.Money(
            amount=Decimal("15.00"),
            currency="SGD"
        ),
        total_amount=value_objects.Money(
            amount=Decimal("120.00"),
            currency="SGD"
        ),
        final_amount=value_objects.Money(
            amount=Decimal("110.50"),
            currency="SGD"
        ),
        shipping_reference="TRACK123",
        coupon_codes=["NEWYEAR2025"],
        status=enums.OrderStatus.PENDING.value
    )

def test_line_item_dto_from_django_model(mock_django_line_item):
    dto = dtos.LineItemDTO.from_django_model(mock_django_line_item)
    assert dto.product_sku == mock_django_line_item.product_sku
    assert dto.product_name == mock_django_line_item.product_name
    assert dto.options["color"] == "red"
    assert dto.package.dimensions == (mock_django_line_item.length, mock_django_line_item.width, mock_django_line_item.height)


def test_order_dto_from_django_model(mock_django_order):
    dto = dtos.OrderDTO.from_django_model(mock_django_order)
    assert dto.order_id == mock_django_order.order_id
    assert dto.destination.city == mock_django_order.delivery_city
    assert len(dto.line_items) == 1
    assert dto.line_items[0].product_name == mock_django_order.line_items.all()[0].product_name

#def test_order_dto_to_domain(domain_order):
#    dto = dtos.OrderDTO.from_domain(domain_order)
#    domain = dto.to_domain()
#
#    assert domain.order_id == domain_order.order_id
#    assert domain.destination.city == domain_order.destination.city
#    assert len(domain.line_items) == 1
#    assert domain.line_items[0].product_name == domain_order.line_items[0].product_name

