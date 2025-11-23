from typing import Protocol


class ShippingWebhookParserAbstract(Protocol):
    def parse(self, payload: dict, headers: dict) -> dict: ... 