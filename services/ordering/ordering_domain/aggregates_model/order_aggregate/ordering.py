from decimal import Decimal
from typing import Optional, List, Set
from ....ordering_domain import abstract_domain_models
from ..buyer_aggregate.buyer import Buyer
from .line_item import LineItem
from .order_status import OrderStatus


class Ordering(abstract_domain_models.AggregateRoot):

    def __init__(self, 
                 entity_id: str,
                 tax_rate: Decimal,
                 buyer: Buyer,
                 line_items: List[LineItem],
                 ):

        self._entity_id = entity_id
        self._tax_rate = tax_rate

        if buyer:
            self._buyer = buyer
        else:
            raise "Unable to process order, missing buyer!"

        #Order Item
        self._order_items = set()
        for line_item in line_items:
            self._line_items.add(line_item)

        self.set_as_waiting_for_payment()        


    def get_line_items(self):
        return self._line_items

    def add_line_item(self, line_item: LineItem) -> None:
        if not line_item:
            raise "No item to add in order!"
        self._line_items.add(line_item)


    def set_as_waiting_for_payment(self):
        self._order_status = OrderStatus.WAITING_FOR_PAYMENT

    def set_as_paid(self):
        self._order_status = OrderStatus.PAID

    def set_tax_rate(self, rate):
        if not rate:
            raise "Invalid tax rate!"
        self._tax_rate = rate

    def get_buyer(self):
        return self._buyer


    #use get method to protect data from external update? 
    def get_tax_rate(self):
        return self._tax_rate
    
    def get_tax_amount(self):
        #amt * (tax_rate / 100)
        pass

    #aggregate?
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

