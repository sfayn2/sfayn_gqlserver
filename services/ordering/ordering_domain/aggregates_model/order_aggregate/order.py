
import abc
from enum import IntEnum
from decimal import Decimal
from typing import Optional, List, Set
from ....ordering_domain import abstract_domain_models
from .order_item import OrderItem
from .customer import Customer
from .address import Address


class OrderStatus(IntEnum):
    WAITING_FOR_PAYMENT = 0
    PAID = 1
    PROCESSING = 2
    PARTIALLY_SHIPPED_OUT = 3 #split shipment
    SHIPPED_OUT = 4
    REFUNDED = 5
    CANCEL = 6
    COMPLETED = 7


class Order(abstract_domain_models.AggregateRoot):

    def __init__(self, 
        entity_id: str = None, 
        order_item: OrderItem,
        address: Address,
        tax_rate: Decimal,
        ):

        self._entity_id = entity_id
        self._order_status = order_status
        self._tax_rate = tax_rate
        self._subtotal = None
        self._total = None 

        #Order Item
        self._order_items = set()

        #Customer
        self._address = address
        self._customer_note = None

    def change_address(self, address: Address):
        self._address  = address

    def change_shipping_method(self, shipping_method: str):
        self._shipping_method = shipping_method

    def add_customer_note(self, customer_note: str):
        self._customer_note = customer_note

    def add_order_item(self, item: OrderItem):
        if not item:
            raise "No selected item!"
        self._order_items.add(order_items)
        return self._order_items

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

