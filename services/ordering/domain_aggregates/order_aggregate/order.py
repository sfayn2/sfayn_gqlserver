
from typing import Optional, List, Set

# TODO
# Order Aggregate root
class Order:

    order_status_id: int  = 0 #WAITING FOR PAYMENT?

    def __init__(self, payment_method_id: int , tax_id: int, customer_id: int, order_items: List[] ):
        self.payment_method_id = payment_method_id
        self.tax_id = tax_id
        self.customer_id = customer_id
        self.order_items = order_items

    def add_order_items(self):
        pass

    def set_paid_status(self):
        if self.order_status_id == 0:
            self.order_status_id = 1 #PAID


    def process_fulfillment_order(self):
        pass