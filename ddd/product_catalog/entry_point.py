import uuid
from datetime import datetime
from ddd.product_catalog.app import message_bus as msgbus, unit_of_work
from ddd.product_catalog.domain import commands, enums

def test_create_category():
    uow = unit_of_work.DjangoUnitOfWork()
    cmd = commands.CreateCategoryCommand(
            id=uuid.uuid4(),
            name="CAT2",
            level="LEVEL_1",
            parent_id=None,
            vendor_name="VENDOR1",
            date_created=datetime.now()
        )

    msgbus.handle(cmd, uow)

def test_activate_product():
    uow = unit_of_work.DjangoUnitOfWork()
    cmd = commands.ActivateProductCommand(
        product_id="2eafd8b6-3539-4ce1-b420-febbf270a889"
    )

    msgbus.handle(cmd, uow)

