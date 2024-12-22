from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
from order_management.domain import value_objects, enums, exceptions


@dataclass
class Order:
    _order_id: str
    _customer_id: str
    _customer_email: str
    _address: value_objects.Address
    _order_lines: List[value_objects.OrderLine]
    _status: enums.OrderStatus = enums.OrderStatus.DRAFT.name
    _shipping_method: str
    _shipping_reference: str
    _shipping_note: str
    _shipping_cost: value_objects.Money
    _total_amount: value_objects.Money
    _payments: List[value_objects.Payment] = field(default_factory=list)
    _date_created: datetime = field(default_factory=datetime.now)
    _date_modified: Optional[datetime] = None

    #VALID_STATUS_TRANSITIONS = {
    #    enums.OrderStatus.DRAFT.name : [enums.OrderStatus.PENDING.name],
    #    enums.OrderStatus.PENDING.name : [enums.OrderStatus.CONFIRMED.name],
    #    enums.OrderStatus.CONFIRMED.name : [enums.OrderStatus.SHIPPED.name, enums.OrderStatus.CANCELLED.name],
    #    enums.OrderStatus.SHIPPED.name : [enums.OrderStatus.COMPLETED.name, enums.OrderStatus.CANCELLED.name],
    #}

    def update_modified_date(self):
        self._date_modified = datetime.now()

    #def change_state(self, new_status: enums.OrderStatus):
    #    if new_status not in self.VALID_STATUS_TRANSITIONS[self._status]:
    #        raise exceptions.InvalidStatusTransitionError(f"Cannot transition from {self._status} to {new_status}")
    #    self._status = new_status
    #    self.update_modified_date()

    def place(self):
        if not self._order_lines:
            raise exceptions.InvalidOrderOperation("Order must have at least one line item.")
        self._status = enums.OrderStatus.PENDING.name
        self.update_modified_date()

    def pay(self):
        if self.status != enums.OrderStatus.PENDING.name:
            raise exceptions.InvalidOrderOperation("Only pending orders can be paid.")
        self._status = enums.OrderStatus.PAID.name
        self.update_modified_date()

    def confirm(self):
        if self.status != "pending":
            raise exceptions.InvalidOrderOperation("Only pending orders can be confirmed.")
        if not self._payment or self._payment.get_amount() < self.get_total_amount():
            raise exceptions.InvalidOrderOperation("Order cannot be confirmed without a full payment.")
        if not self._shipping_reference:
            raise exceptions.InvalidOrderOperation("Shipping reference is missing.")
        self._status = enums.OrderStatus.CONFIRMED.name
        self.update_modified_date()

    def ship(self):
        if self._status != "confirmed":
            raise exceptions.InvalidOrderOperation("Only confirm order can be ship.")
        self._status = enums.OrderStatus.SHIPPED.name
        self.update_modified_date()

    def cancel(self):
        if self._status in ("completed", "cancelled"):
            raise exceptions.InvalidOrderOperation("Cannot cancel a completed or already cancelled order")
        self._status = enums.OrderStatus.CANCELLED.name
        self.update_modified_date()
    
    def complete(self):
        if self._status != "shipped":
            raise exceptions.InvalidOrderOperation("Only shipped order can be completed")
        self._status = enums.OrderStatus.COMPLETED.name
        self.update_modified_date()

    def get_total_amount(self):
        return sum(line.total_price for line in self._order_lines)

    def get_total_paid(self):
        return sum(payment.get_amount() for payment in self.payments)

    @property
    def is_fully_paid(self):
        return self.get_total_paid >= self.get_total_amount()
    
    def apply_payment(self, payment: value_objects.Payment):
        #if payment.get_amount() < self.get_total_amount():
        #    raise exceptions.InvalidOrderOperation("Insufficient payment amount")
        self._payments.append(payment)
        if self.is_fully_paid:
            self._status = enums.OrderStatus.PAID.name

    

