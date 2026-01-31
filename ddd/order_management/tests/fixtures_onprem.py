import pytest, boto3, os
from unittest.mock import MagicMock, PropertyMock
from django.db import connection
from .fixtures import *
from .data import *
from order_management import models as django_snapshots

@pytest.fixture
def fake_get_user_context():    
    return 'ddd.order_management.infrastructure.access_control1.AccessControl1.get_user_context'

@pytest.fixture(scope="session", autouse=True)
def seeded_all(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        # Temporarily disable for bulk seed if needed, 
        # but the unpacking below fixes the ORD-CONFIRMED-1 error
        #with connection.cursor() as cursor:
        #    cursor.execute("PRAGMA foreign_keys = OFF;")

        # 2. SaaS Configs
        for sas in SAAS_CONFIG_SEEDS:
            t_id, configs, dt = sas
            django_snapshots.SaaSConfig.objects.create(
                tenant_id=t_id, configs=configs, last_update_dt=dt
            )

        # 1. Tenant Configs
        for tc in TENANT_CONFIG_SEEDS:
            t_id, configs, dt = tc
            django_snapshots.TenantConfig.objects.create(
                tenant_id=t_id, configs=configs, last_update_dt=dt
            )


        # 3. User Authorizations
        for us in USER_SEEDS:
            t_id, perm, scope, active = us
            django_snapshots.UserAuthorizationSnapshot.objects.create(
                tenant_id=t_id, permission_codename=perm, scope=scope, is_active=active
            )

        # 4. Orders
        for os_data in ORDER_SEEDS:
            (oid, tid, ver, ref, stat, cid, cname, cmail, pstat, curr, cdt, mdt) = os_data
            django_snapshots.Order.objects.create(
                order_id=oid, tenant_id=tid, version=ver, external_ref=ref,
                order_status=stat, customer_id=cid, customer_name=cname,
                customer_email=cmail, payment_status=pstat, currency=curr,
                date_created=cdt, date_modified=mdt
            )

        # 5. Line Items
        for ol in ORDER_LINE_SEEDS:
            oid, sku, name, price, curr, qty, vid, weight = ol
            django_snapshots.LineItem.objects.create(
                order_id=oid, product_sku=sku, product_name=name,
                product_price=price, product_currency=curr,
                order_quantity=qty, vendor_id=vid, package_weight_kg=weight
            )

        # 6. Shipments
        for sh in SHIPMENT_SEEDS:
            (sid, oid, l1, l2, city, post, country, state, prov, track, amt, curr, stat) = sh
            django_snapshots.Shipment.objects.create(
                shipment_id=sid, order_id=oid, shipment_address_line1=l1,
                shipment_address_line2=l2, shipment_address_city=city,
                shipment_address_postal=post, shipment_address_country=country,
                shipment_address_state=state, shipment_provider=prov,
                tracking_reference=track, shipment_amount=amt,
                shipment_currency=curr, shipment_status=stat
            )

        # 7. Shipment Items (Uses specific Shipment IDs, not Order IDs)
        for shi in SHIPMENT_ITEM_SEEDS:
            item_id, order_id, ship_id, sku, qty = shi
            django_snapshots.ShipmentItem.objects.create(
                shipment_item_id=item_id, 
                shipment_id=ship_id, # This correctly maps to "SH-1" index
                line_item_id=sku, 
                quantity=qty, 
            )

        # 8. User Action Logs
        for ual in USER_ACTION_SEEDS:
            oid, act, by, inp, ts = ual
            django_snapshots.UserActionLog.objects.create(
                order_id=oid, action=act, performed_by=by, 
                user_input=inp, executed_at=ts
            )

        # Re-enable to ensure data integrity during test execution
        #with connection.cursor() as cursor:
        #    cursor.execute("PRAGMA foreign_keys = ON;")

@pytest.fixture
def mock_context_w_auth_header_token(fake_jwt_valid_token):
    # Create a mock object that looks like a Django request object for context passing
    mock_context = MagicMock()
    # Ensure the 'META' attribute behaves like a dictionary
    type(mock_context).META = PropertyMock(return_value={
        "HTTP_AUTHORIZATION": f"Bearer {fake_jwt_valid_token}"
    })

    return mock_context