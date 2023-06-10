
import abc
from typing import Optional, List, Set
from .order_item import OrderItem
from .customer import Customer
from enum import Enum
from decimal import Decimal

class AggregateRoot(abc.ABC):
    pass


class OrderStatus(Enum):
    WAITING_FOR_PAYMENT = 0
    PAID = 1
    PROCESSING = 2
    PARTIALLY_SHIPPED_OUT = 3 #split shipment
    SHIPPED_OUT = 4
    REFUNDED = 5
    CANCEL = 6
    COMPLETED = 7


class PendingPaymentException(exception):
    pass

order = Order(order_id=1, order_status=0, )
order.set_paid_status()
order.tax_rate = 1
# TODO
# Order Aggregate root
class Order(AggregateRoot):

    def __init__(self, 
        order_id: int, 
        order_status: OrderStatus.WAITING_FOR_PAYMENT,
        order_item: OrderItem,
        customer: Customer
        ):

        self.order_id = order_id
        self.order_status = order_status
        self.order_item = order_item
        self.customer = customer

    def add_order_items(self, order_items: List[OrderItem]):
        self.order_item.add(order_items)

    def set_customer_note(self, customer_note: str):
        self.customer_note = customer_note

    def set_tax_rate(self, rate: Decimal):
        self.tax_rate = rate

    def set_tax_amount(self, amt):
        self.tax_amount = amt

    def set_paid_status(self, payment_status: int):
        if self.order_status == OrderStatus.WAITING_FOR_PAYMENT and payment_status == 'PAID': #TODO enum?
            self.order_status = OrderStatus.PAID
        else:
            raise PendingPaymentException(f"Pending customer payment for order ref: {self.order_id}")

    def set_shipped_status(self):
        pass

    def set_cancelled_status(self):
        pass

    def set_completed_status(self):
        pass
    
    def get_total(self):
        pass


    def process_fulfillment_order(self):
        pass