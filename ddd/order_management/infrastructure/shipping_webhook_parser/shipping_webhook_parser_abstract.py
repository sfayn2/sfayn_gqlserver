from __future__ import annotations
from typing import Protocol, Any
from ddd.order_management.application import dtos


class ShippingWebhookParserAbstract(Protocol):
    def parse(self, payload: dict[str, Any]) -> dtos.ShippingWebhookDTO: ...