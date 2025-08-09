from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_product_update_from_external(
    command: commands.PublishProductUpdateCommand, 
    product_update_publisher: ports.EventPublisherAbstract
):

    product_update_publisher.publish(
        command
    )

    print(f"Product update has been published  {event_payloads}")
