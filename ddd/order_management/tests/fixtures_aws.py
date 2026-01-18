import pytest, boto3, os
from decimal import Decimal 
from .fixtures import *
from .data import *


@pytest.fixture
def fake_get_user_context():    
    return 'ddd.order_management.infrastructure.access_control1.DynamodbAccessControl1.get_user_context'

# =================
# Seeded Fixtures
# ==============
@pytest.fixture(scope="session", autouse=True)
def seeded_all():
    """
    Equivalent seeder for DynamoDB using Single Table Design.
    """
    # Use environment variables for LocalStack flexibility
    table_name = os.getenv("DYNAMODB_TABLE_NAME")
    
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    

    # Lets PreWipe the table first
    # Scan for all keys
    scan = table.scan(ProjectionExpression='pk, sk')
    
    # Batch delete to stay fast
    with table.batch_writer() as batch:
        for each in scan.get('Items', []):
            batch.delete_item(Key={'pk': each['pk'], 'sk': each['sk']})
    # Lets PreWipe the table first

    # Batch writer handles buffering and efficiency
    with table.batch_writer() as batch:
        

        # 1. Tenant Configs
        for tc in TENANT_CONFIG_SEEDS:
            batch.put_item(Item={
                "pk": f"TENANT#{tc[0]}", 
                "sk": "CONFIG#TENANT",
                "configs": tc[1], 
                "last_update_dt": tc[2].isoformat() if hasattr(tc[2], 'isoformat') else tc[2]
            })

        # 2. SaaS Configs
        for sas in SAAS_CONFIG_SEEDS:
            batch.put_item(Item={
                "pk": f"TENANT#{sas[0]}", 
                "sk": "CONFIG#SAAS",
                "configs": sas[1], 
                "last_update_dt": sas[2].isoformat() if hasattr(sas[2], 'isoformat') else sas[2]
            })

        # 3. User Authorizations
        for us in USER_SEEDS:
            batch.put_item(Item={
                "pk": f"TENANT#{us[0]}", 
                "sk": f"AUTH#USER#{us[1]}",
                "scope": us[2],
                "is_active": us[3]
            })

        # 4. Orders (The Header)
        for os_data in ORDER_SEEDS:
            batch.put_item(Item={
                "pk": f"TENANT#{os_data[1]}", 
                "sk": f"ORDER#{os_data[0]}",
                "order_id": os_data[0],
                "tenant_id": os_data[1],   
                "version": os_data[2],
                "external_ref": os_data[3],
                "order_status": os_data[4],
                "customer_id": os_data[5],
                "customer_name": os_data[6],
                "customer_email": os_data[7],
                "payment_status": os_data[8],
                "currency": os_data[9],
                "date_created": os_data[10].isoformat(),
                "date_modified": os_data[11].isoformat(),
                "entity_type": "ORDER"
            })

        # 5. Order Lines
        for ol in ORDER_LINE_SEEDS:
            batch.put_item(Item={
                "pk": f"ORDER#{ol[0]}", 
                "sk": f"LINE#{ol[1]}",
                "product_sku": ol[1],  
                "product_name": ol[2],
                "product_price": Decimal(str(ol[3])),
                "product_currency": ol[4],
                "order_quantity": ol[5],
                "vendor_id": ol[6],
                "package_weight_kg": Decimal(str(ol[7])),
                "entity_type": "LINE_ITEM"
            })

        # 6. Shipments
        for sh in SHIPMENT_SEEDS:
            batch.put_item(Item={
                "pk": f"ORDER#{sh[1]}", 
                "sk": f"SHIPMENT#{sh[0]}",
                "line1": sh[2],
                "line2": sh[3],
                "city": sh[4],
                "postal": sh[5],
                "country": sh[6],
                "state": sh[7],
                "provider": sh[8],
                "tracking": sh[9],
                "amount": Decimal(str(sh[10])),
                "currency": sh[11],
                "status": sh[12],
                "entity_type": "SHIPMENT"
            })


        # 7. Shipment Items (Flattened in DynamoDB)
        for shi in SHIPMENT_ITEM_SEEDS:
            batch.put_item(Item={
                # PK is still the Order ID so we can fetch everything at once
                "pk": f"ORDER#{shi[1]}", # Assuming index 4 is OrderID, or look it up from Shipment
                # Hierarchical SK to group items under their specific shipment
                "sk": f"SHIPMENT#{shi[2]}#ITEM#{shi[0]}#SKU#{shi[3]}",
                "shipment_id": shi[2],
                "shipment_item_id": shi[0],
                "line_item_sku": shi[3], 
                "quantity": shi[4],
                "entity_type": "SHIPMENT_ITEM"
            })


        # 8. User Action Logs
        for ual in USER_ACTION_SEEDS:
            batch.put_item(Item={
                "pk": f"ORDER#{ual[0]}", 
                "sk": f"LOG#{ual[4].isoformat()}#{ual[1]}",
                "action": ual[1],
                "performed_by": ual[2],
                "user_input": ual[3]
            })
    print("✅ DynamoDB Seeding Complete.")

