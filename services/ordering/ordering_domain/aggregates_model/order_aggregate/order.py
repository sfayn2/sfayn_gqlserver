
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


class PendingPaymentException(Exception):
    pass

class NoSelectedItemsException(Exception):
    pass

class Order(abstract_domain_models.AggregateRoot):

    def __init__(self, 
        entity_id: str, 
        order_status: OrderStatus.WAITING_FOR_PAYMENT,
        address: Address
        ):

        self.entity_id = entity_id
        self.order_status = order_status
        self.address = address

    def add_order_items(self, order_items: List[OrderItem]):
        if not order_items:
            raise NoSelectedItemsException(f'Unable to add order items {self.entity_id}')
        order_item = OrderItem()
        order_item.add(order_items)
        return order_item

    def set_customer(self, customer, customer_note: str):
        #optional?
        #customer = customer_repo()
        self.customer_note = customer_note

    def set_tax_rate(self, rate: Decimal):
        self.tax_rate = rate

    def set_amount_paid(self):
        pass

    def set_order_status_paid(self, payment_status: int):
        if self.order_status == OrderStatus.WAITING_FOR_PAYMENT and payment_status == 'PAID': #TODO enum?
            self.order_status = OrderStatus.PAID
        else:
            raise PendingPaymentException(f"Pending customer payment for order ref: {self.entity_id}")

    def set_order_status_shipped(self):
        pass

    def set_order_status_cancelled(self):
        pass

    def set_order_status_completed(self):
        pass
    
    def get_tax_amount(self):
        #amt * (tax_rate / 100)
        pass

    def get_subtotal(self):
        pass

    def get_total(self):
        pass


    def process_fulfillment_order(self):
        pass