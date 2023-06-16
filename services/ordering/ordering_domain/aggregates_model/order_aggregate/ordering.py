
import abc
from enum import IntEnum
from decimal import Decimal
from typing import Optional, List, Set
from ....ordering_domain import abstract_domain_models
from .line_item import OrderItem


class OrderStatus(IntEnum):
    WAITING_FOR_PAYMENT = 0
    PAID = 1
    PROCESSING = 2
    PARTIALLY_SHIPPED_OUT = 3 #split shipment
    SHIPPED_OUT = 4
    REFUNDED = 5
    CANCEL = 6
    COMPLETED = 7


class Ordering(abstract_domain_models.AggregateRoot):

    def __init__(self, 
        entity_id: str = None, 
        tax_rate: Decimal,
        ):

        self._entity_id = entity_id
        self._tax_rate = tax_rate

        #Order Item
        self._order_items = set()

        #Order Fulfillment
        self._order_fulfillments = set()

        #Buyer
        self._buyer_note = None
        self._payment_status = None

    def add_buyer_note(self, buyer_note: str):
        self._buyer_note = buyer_note

    def add_order_item(self, item: OrderItem):
        if not item:
            raise "No item to add in order!"
        self._order_items.add(order_items)

    def get_order_items(self):
        return self._order_items

    def place_order(self, buyer: Buyer):

        self._payment_status = buyer.process_payment(
            self.get_total()
        )
        if self._payment_status  == OrderStatus.PAID:
            self.set_as_paid()
        else:
            self.set_as_waiting_for_payment()


    def set_as_waiting_for_payment(self):
        self._order_status = OrderStatus.WAITING_FOR_PAYMENT

    def set_as_paid(self)
        self._order_status = OrderStatus.PAID
    

    def change_order_status(self, payment_status: int):
        #TODO
        if self.order_status == OrderStatus.WAITING_FOR_PAYMENT and payment_status == 'PAID': #TODO enum?
            self.order_status = OrderStatus.PAID
        else:
            raise "Pending customer payment!"

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
            subtotal += (item.product_quantity * item.product_price) - item.discounts_fee
        return subtotal

    def get_total(self):
        #TODO calculate based on collection of order items
        total = 0.0
        return total

