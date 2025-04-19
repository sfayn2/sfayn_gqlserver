from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from ddd.order_management.domain import models, value_objects

class OrderServiceAbstract(ABC):

    @abstractmethod
    def confirm_order(self, payment_details: value_objects.PaymentDetails,
                    order: models.Order) -> models.Order:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def create_draft_order(
            self,
            customer_details: value_objects.CustomerDetails,
            shipping_address: value_objects.Address,
            line_items: List[models.LineItem]
    ) -> models.Order:
        raise NotImplementedError("Subclasses must implement this method")
