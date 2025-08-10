from __future__ import annotations
import json
from ddd.order_management.application import (
    ports, 
    dtos
)
from ddd.order_management.domain import events, exceptions

def handle_publish_product_update(
    command: commands.PublishProductUpdateCommand, 
    event_publisher: ports.EventPublisherAbstract
):
    event = dtos.ProductUpdateIntegrationEvent(
        **command.model_dump()
    )

    event_publisher.publish(event)

    print(f"Product update has been published  {event}")
