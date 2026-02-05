import json
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from ddd.order_management.domain import (
    enums
)

# === Test Data ========
USER1 = "7494d733-5030-4979-8aa9-637571f533a7" #equivalent to sub in JWT
USER2 = "user-2"

USERNAME1 = "pao" #equivalent to username in JWT

SAAS1 = "saas_123"
TENANT1 = "tenant_123"
TENANT2 = "tenant_456"
VENDOR1 = "vendor-1"
VENDOR2 = "vendor-2"

VENDOR_PERMISSIONS = [
    "add_order",
    "cancel_order",
    "add_shipment",
    "cancel_shipment",
    "confirm_shipment",
    "deliver_shipment",
    "mark_as_completed",
    "get_order",
    # Add more permissions here easily
]

# Generate the USER_SEEDS tuple using a generator expression
# Columns tenant_id, permission_codename, scope, is_active
USER_SEEDS = tuple(
    (TENANT1, permission, json.dumps({ "role": ["vendor"] }), True)
    for permission in VENDOR_PERMISSIONS
)
#USER_SEEDS = (
#    (TENANT1, "add_shipment", json.dumps({ "role": ["vendor"] }), True),
#    (TENANT1, "add_order", json.dumps({ "role": ["vendor"] }), True),
#    (TENANT1, "cancel_order", json.dumps({ "role": ["vendor"] }), True),
#    (TENANT1, "cancel_shipment", json.dumps({ "role": ["vendor"] }), True),
#)

# Columns order_id, tenant_id, version, external_ref, order_status, customer_id, customer_name, customer_email, payment_status, currency, date_created, date_modified
ORDER_SEEDS = (
    ("ORD-CONFIRMED-1", TENANT1, 1, "external ref here", enums.OrderStatus.CONFIRMED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)), 
    ("ORD-NOTCONFIRMED-1", TENANT1, 1, "external ref here", enums.OrderStatus.PENDING.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-DRAFT-1", TENANT1, 1, "external ref here", enums.OrderStatus.DRAFT.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-CONFIRMED_W_SHIPPED-1", TENANT1, 1, "external ref here", enums.OrderStatus.SHIPPED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-CONFIRMED_W_PENDING-1", TENANT1, 1, "external ref here", enums.OrderStatus.PENDING.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-CONFIRMED_W_CONFIRMED-1", TENANT1, 1, "external ref here", enums.OrderStatus.CONFIRMED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-CONFIRMED_W_DELIVERED-1", TENANT1, 1, "external ref here", enums.OrderStatus.DELIVERED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-READY-TO-COMPLETE-1", TENANT1, 1, "external ref here", enums.OrderStatus.DELIVERED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.PAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-ALREADY-COMPLETED-1", TENANT1, 1, "external ref here", enums.OrderStatus.COMPLETED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.PAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-READY-TO-COMPLETE-UNPAID-1", TENANT1, 1, "external ref here", enums.OrderStatus.DELIVERED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.UNPAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
    ("ORD-READY-TO-COMPLETE-PAID-1", TENANT1, 1, "external ref here", enums.OrderStatus.DELIVERED.value, "customer id here", " customer name", " customer email", enums.PaymentStatus.PAID.value, "SGD", datetime.now(timezone.utc), datetime.now(timezone.utc)),
)

# Columns order_id, product_sku, product_name, product_price, product_currency, order_quantity, vendor_id, package_weight_kg
ORDER_LINE_SEEDS = (
    ("ORD-CONFIRMED-1", "SKU-A", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-CONFIRMED-1", "SKU-B", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-NOTCONFIRMED-1", "SKU-NOTCONFIRMED", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-CONFIRMED_W_SHIPPED-1", "SKU-C", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-CONFIRMED_W_PENDING-1", "SKU-D", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-CONFIRMED_W_CONFIRMED-1", "SKU-E", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-CONFIRMED_W_DELIVERED-1", "SKU-F", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-READY-TO-COMPLETE-1", "SKU-G", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-ALREADY-COMPLETED-1", "SKU-H", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-READY-TO-COMPLETE-UNPAID-1", "SKU-I", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
    ("ORD-READY-TO-COMPLETE-PAID-1", "SKU-J", "my product", Decimal("1.12"), "SGD", 2, VENDOR1, Decimal("20")),
)

# Shipment
# Columns shipment_id, order_id, shipment_address_line1, shipment_address_line2, shipment_address_city, shipment_address_postal, shipment_address_country, shipment_address_state, shipment_provider, tracking_reference, shipment_amount, shipment_currency, shipment_status, tenant_id
SHIPMENT_SEEDS = (
    ("SH-1", "ORD-CONFIRMED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.PENDING.value, TENANT1),
    ("SH-SHIPPED-SHIPPED-1", "ORD-CONFIRMED_W_SHIPPED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", "TN123456789", Decimal("2.2"), "SGD", enums.ShipmentStatus.SHIPPED.value, TENANT1),
    ("SH-SHIPPED-SHIPPED-2", "ORD-CONFIRMED_W_SHIPPED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", "TN123456790", Decimal("2.2"), "SGD", enums.ShipmentStatus.SHIPPED.value, TENANT1),
    ("SH-SHIPPED-PENDING-1", "ORD-CONFIRMED_W_SHIPPED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", "TN123456791", Decimal("2.2"), "SGD", enums.ShipmentStatus.PENDING.value, TENANT1),
    ("SH-SHIPPED-CONFIRMED-1", "ORD-CONFIRMED_W_SHIPPED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", "TN123456792", Decimal("2.2"), "SGD", enums.ShipmentStatus.CONFIRMED.value, TENANT1),
    ("SH-PENDING-2", "ORD-CONFIRMED_W_PENDING-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD" , enums.ShipmentStatus.PENDING.value, TENANT1),
    ("SH-CONFIRMED-2", "ORD-CONFIRMED_W_CONFIRMED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.CONFIRMED.value, TENANT1),
    ("SH-DELIVERED-2", "ORD-CONFIRMED_W_DELIVERED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.DELIVERED.value, TENANT1),
    ("SH-READY-TO-COMPLETE-1", "ORD-READY-TO-COMPLETE-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.DELIVERED.value, TENANT1),
    ("SH-ALREADY-COMPLETED-1", "ORD-ALREADY-COMPLETED-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD", enums.ShipmentStatus.DELIVERED.value, TENANT1),
    ("SH-READY-TO-COMPLETE-UNPAID-1", "ORD-READY-TO-COMPLETE-UNPAID-1", "line 1", "line 2", "city ", "postal here", "country here", "state here", "provider here", " tracking reference here", Decimal("2.2"), "SGD" , enums.ShipmentStatus.DELIVERED.value, TENANT1),
    ("SH-READY-TO-COMPLETE-PAID-1","ORD-READY-TO-COMPLETE-PAID-1","line 1","line 2","city ","postal here","country here","state here","provider here"," tracking reference here" ,Decimal("2.2"),"SGD" ,enums.ShipmentStatus.DELIVERED.value,TENANT1),
)


# Shipment Item
# Columns shipment_item_id, order_id, shipment_id, line_item_id, quantity
SHIPMENT_ITEM_SEEDS = (
    ("SHI-1", "ORD-CONFIRMED-1", "SH-1", "SKU-A", 1),
    ("SHI-SHIPPED-1", "ORD-CONFIRMED_W_SHIPPED-1", "SH-SHIPPED-SHIPPED-1", "SKU-C", 1),
    ("SHI-SHIPPED-2", "ORD-CONFIRMED_W_SHIPPED-1", "SH-SHIPPED-PENDING-1", "SKU-C", 1),
    ("SHI-SHIPPED-3", "ORD-CONFIRMED_W_SHIPPED-1", "SH-SHIPPED-CONFIRMED-1", "SKU-C", 1),
    ("SHI-SHIPPED-4", "ORD-CONFIRMED_W_SHIPPED-1", "SH-SHIPPED-SHIPPED-2", "SKU-C", 1),
    ("SHI-PENDING-1", "ORD-CONFIRMED_W_PENDING-1", "SH-PENDING-2", "SKU-D", 1),
    ("SHI-CONFIRMED-1", "ORD-CONFIRMED_W_CONFIRMED-1", "SH-CONFIRMED-2", "SKU-E", 1),
    ("SHI-DELIVERED-1", "ORD-CONFIRMED_W_DELIVERED-1", "SH-DELIVERED-2", "SKU-F", 1),
    ("SHI-READY-TO-COMPLETE-1", "ORD-READY-TO-COMPLETE-1", "SH-READY-TO-COMPLETE-1", "SKU-G", 1),
    ("SHI-ALREADY-COMPLETED-1", "ORD-ALREADY-COMPLETED-1", "SH-ALREADY-COMPLETED-1", "SKU-H", 1),
    ("SHI-READY-TO-COMPLETE-UNPAID-1", "ORD-READY-TO-COMPLETE-UNPAID-1", "SH-READY-TO-COMPLETE-UNPAID-1", "SKU-I", 1),
    ("SHI-READY-TO-COMPLETE-PAID-1", "ORD-READY-TO-COMPLETE-PAID-1", "SH-READY-TO-COMPLETE-PAID-1", "SKU-J", 1),
)

# UserActionLog
# Columns order_id, action, performed_by, user_input, executed_at
USER_ACTION_SEEDS = (
    ("ORD-CONFIRMED-1", "add_order", USER1, json.dumps({}), datetime.now(timezone.utc)),
    ("ORD-CONFIRMED_W_SHIPPED-1", "cancel_order", USER1, json.dumps({}), datetime.now(timezone.utc)),
)

# TenantConfig
# Columns tenant_id, configs, last_update_dt
TENANT_CONFIG_SEEDS  = (
    (TENANT1, json.dumps({
        "restocking_fee_percent": 10,
        "max_refund_amount": 500.0,
    }), datetime.now(timezone.utc)),
)

# SaaSConfig
# Columns tenant_id, configs, last_update_dt
SAAS_CONFIG_SEEDS  = (
    (SAAS1, json.dumps({
        "idp": {},
        "webhooks": {
            "shipment_tracker": {
                "provider": "wss",
                "shared_secret": "2323434235235",
                "max_age_seconds": 3000,
                "tracking_reference_jmespath": "tracking_number",
            },
            "add_order": {
                "provider": "wss",
                "shared_secret": "2323434235235",
                "max_age_seconds": 3000,
            }
        },
        "create_shipment_api": {
            "provider": "wss",
            "api_key": "api key",
            "endpoint": "https://endpoint.dev",
        }
    }), datetime.now(timezone.utc)),
    (TENANT1, json.dumps({
        "idp": {
            "public_key": "http://keycloak_main:8080/realms/TenantOMSAPI-Realm/protocol/openid-connect/certs",
            "issuer": "http://localhost:8080/realms/TenantOMSAPI-Realm",
            "audience": "TenantOMSAPI-Client",
            "algorithm": "RS256",
            "token_type": "Bearer", 
        },
        "webhooks": {
            "shipment_tracker": {
                "provider": "wss",
                "shared_secret": "2323434235235",
                "max_age_seconds": 3000,
                "tracking_reference_jmespath": "result.tracking_code || data.tracking_code",
            },
            "add_order": {
                "provider": "wss",
                "shared_secret": "2323434235235",
                "max_age_seconds": 3000,
            }
        },
        "create_shipment_api": {
            "provider": "wss",
            "api_key": "api key",
            "endpoint": "https://endpoint.dev",
        }
    }), datetime.now(timezone.utc)),
)

# === Test Data ========

JWT_VENDOR_PAYLOAD = {
    "exp": datetime.now() + timedelta(minutes=5),
    "iat": datetime.now(),
    "jti": "onrtro:cbe35fc0-4bd2-8af7-e403-6aacbf565d51",
    "iss": "http://localhost:8080/realms/TenantOMSAPI-Realm",
    "aud": "TenantOMSAPI-Client",
    "sub": "7494d733-5030-4979-8aa9-637571f533a7",
    "typ": "Bearer",
    "azp": "TenantOMSAPI-Client",
    "sid": "0FlQ-6gO1EE66LvRQ9SxDqsJ",
    "scope": "openid organization",
    "organization": [
        TENANT1
    ],
    "roles": [
        "vendor"
    ],
    "username": USERNAME1
    }

JWT_EXPIRED_CUSTOMER_PAYLOAD = {
    "exp": datetime.now() - timedelta(minutes=5),
    "iat": datetime.now(),
    "jti": "onrtro:cbe35fc0-4bd2-8af7-e403-6aacbf565d51",
    "iss": "http://localhost:8080/realms/TenantOMSAPI-Realm",
    "aud": "TenantOMSAPI-Client",
    "sub": "7494d733-5030-4979-8aa9-637571f533a7",
    "typ": "Bearer",
    "azp": "TenantOMSAPI-Client",
    "sid": "0FlQ-6gO1EE66LvRQ9SxDqsJ",
    "scope": "openid organization",
    "organization": [
        TENANT1
    ],
    "roles": [
        "customer"
    ],
    "username": USERNAME1
    }