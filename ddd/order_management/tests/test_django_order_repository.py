import pytest
from datetime import datetime
from unittest import mock
from decimal import Decimal
from ddd.order_management.infrastructure import django_order_repository, order_dtos
from ddd.order_management.domain import models, value_objects, enums

@pytest.fixture
def mock_django_line_item():
    mck = mock.MagicMock()
    mck.product_sku = "SKU123"
    mck.product_name = "Test Product"
    mck.vendor_name = "VENDOR1"
    mck.product_category = "Category1"
    mck.options = '{"color": "red", "size": "m" }'
    mck.product_price = Decimal("50.00")
    mck.currency = "SGD"
    mck.order_quantity = 2
    mck.weight = Decimal("1.5")
    mck.length = 10
    mck.width = 5
    mck.height = 5
    mck.is_free_gift = False
    mck.is_taxable = True
    return mck

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
    mck = mock.MagicMock()
    mck.order_id = "ORDER123"
    mck.date_created = datetime(2025, 1, 1, 12, 0, 0)
    mck.date_modified = datetime(2025, 1, 2, 12, 0, 0)
    mck.delivery_street = "123 Main St"
    mck.delivery_city = "New York"
    mck.delivery_postal = 10001
    mck.delivery_state = "NY"
    mck.delivery_country = "USA"
    mck.customer_first_name = "John"
    mck.customer_last_name = "Doe"
    mck.customer_email = "john.doe@example.com"
    mck.shipping_method = enums.ShippingMethod.STANDARD.value
    mck.shipping_delivery_time = "3-5 business days"
    mck.shipping_cost = Decimal("10.00")
    mck.currency = "SGD"
    mck.payment_method = enums.PaymentMethod.PAYPAL.value
    mck.payment_reference = "PAY123"
    mck.payment_amount = Decimal("110.50")
    mck.cancellation_reason = ""
    mck.total_discounts_fee = Decimal("5.00")
    mck.offer_details = "New Year Offer"
    mck.tax_details = "Tax Included"
    mck.tax_amount = Decimal("15.00")
    mck.total_amount = Decimal("120.00")
    mck.final_amount = Decimal("110.50")
    mck.shipping_tracking_reference = "TRACK123"
    mck.coupon_codes = ["NEWYEAR2025"]
    mck.status = enums.OrderStatus.PENDING.value
    mck.line_items.all.return_value = [mock_django_line_item]
    return mck

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
    dto = order_dtos.LineItemDTO.from_django_model(mock_django_line_item)
    assert dto.product_sku == mock_django_line_item.product_sku
    assert dto.product_name == mock_django_line_item.product_name
    assert dto.options["color"] == "red"
    assert dto.package.dimensions == (mock_django_line_item.length, mock_django_line_item.width, mock_django_line_item.height)


def test_order_dto_from_django_model(mock_django_order):
    dto = order_dtos.OrderDTO.from_django_model(mock_django_order)
    assert dto.order_id == mock_django_order.order_id
    assert dto.destination.city == mock_django_order.delivery_city
    assert len(dto.line_items) == 1
    assert dto.line_items[0].product_name == mock_django_order.line_items.all()[0].product_name

def test_order_dto_to_domain(domain_order):
    dto = order_dtos.OrderDTO.from_domain(domain_order)
    domain = dto.to_domain()

    assert domain.order_id == domain_order.order_id
    assert domain.destination.city == domain_order.destination.city
    assert len(domain.line_items) == 1
    assert domain.line_items[0].product_name == domain_order.line_items[0].product_name

def test_get_order(mock_django_order):
    mock_django_order2 = order_dtos.OrderDTO.from_django_model(mock_django_order)
    mock_to_domain = mock_django_order2.to_domain()
    with mock.patch("order_management.models.Order.objects.get", return_value=mock_django_order) as mock_get:
        
        repository = django_order_repository.DjangoOrderRepository()
        result = repository.get(order_id=1)

        mock_get.assert_called_once_with(order_id=1)

        assert result.order_id == mock_to_domain.order_id
        assert result.destination == mock_to_domain.destination
        assert result.payment_details == mock_to_domain.payment_details
        assert result.shipping_details == mock_to_domain.shipping_details
        #assert result.line_items == mock_to_domain.line_items
