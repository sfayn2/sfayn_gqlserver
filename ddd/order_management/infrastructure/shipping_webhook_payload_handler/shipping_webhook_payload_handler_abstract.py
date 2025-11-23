from typing import Protocol


class ShippingWebhookPayloadHandlerAbstract(Protocol):
    def parse(self, payload: dict, headers: dict) -> dict: ... 