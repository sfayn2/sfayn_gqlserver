from decimal import Decimal
from typing import Optional, List
from ....ordering_domain import abstract_domain_models
from ..buyer_aggregate.buyer import Buyer
from .line_item import LineItem
from .fulfillment_item import FulfillmentItem, FulfillmentStatus
from .money import Money
from .order_status import OrderStatus


class Ordering(abstract_domain_models.AggregateRoot):

    def __init__(self, 
                 entity_id: str,
                 tax_amount: Money,
                 buyer: Buyer,
                 line_items: List[LineItem],
                 currency: str,
                 payment_status: bool
                 ):

        self._entity_id = entity_id
        self._tax_amount = tax_amount
        self._currency = currency
        self._payment_status = payment_status

        if buyer:
            self._buyer = buyer
        else:
            raise "Unable to process order, missing buyer!"

        #Order Item
        for line_item in line_items:
            self.add_line_item(line_item)

    
    def as_dict(self):
        return {
            "discounts_fee": self.get_discounts_fee(),
            "tax_amount": self.get_tax_amount(),
            "sub_total": self.get_subtotal(),
            "total": self.get_total(),
            "currency": self.get_currency(),
            "status": self.get_order_status(),
            "buyer_id": self._buyer.get_buyer_id(),
            "buyer_note": self._buyer.get_buyer_note(),
        }


    def get_line_items(self):
        return self._line_items

    def get_currency(self):
        return self._currency

    def add_line_item(self, line_item: LineItem) -> None:
        if not line_item:
            raise "No item to add in order!"
        self._line_items.add(line_item)

    def set_fulfillment_items(self) -> None:
        if not self._line_items:
            raise "No item to fulfill!"
        #TODO: create fulfilmment datagg
        self._fulfillment_items = self.add_line_items

    def get_fulfillment_items(self) -> List[FulfillmentItem]:
        return self._fulfillment_items

    def get_order_status(self):
        if self._payment_status == True:

            aggregate_status = [FulfillmentStatus.CANCELLED, 
                                FulfillmentStatus.NOT_FULFILLED, 
                                FulfillmentStatus.PROCESSING, 
                                FulfillmentStatus.FULFILLED]

            for status in aggregate_status:
                for fulfill_item in self.get_fulfillment_items():
                    if fulfill_item.get_fulfillment_status() == status:
                        if status == FulfillmentStatus.CANCELLED:
                            self._order_status = OrderStatus.CANCEL
                        elif status == FulfillmentStatus.NOT_FULFILLED:
                            self._order_status = OrderStatus.PAID
                        elif status == FulfillmentStatus.PROCESSING:
                            self._order_status = OrderStatus.PROCESSING
                        elif status == FulfillmentStatus.FULFILLED:
                            self._order_status = OrderStatus.COMPLETED
                        return self._order_status

            self._order_status = OrderStatus.PAID
        else:
            self._order_status = OrderStatus.WAITING_FOR_PAYMENT    


    def get_tax_amount(self):
        return self._tax_amount

    def get_subtotal(self):
        #calculate based on collection of order items
        subtotal = 0.0
        for item in self._order_items:
            subtotal += (item.quantity * item.price) - item.discounts_fee
        return subtotal

    def get_total(self):
        #TODO calculate based on collection of order items
        total = 0.0
        return total

