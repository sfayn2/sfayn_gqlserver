from abc import ABC
from typing import List
from dataclasses import dataclass
from pydantic import BaseModel
from ddd.order_management.domain import value_objects, models, enums
from ddd.order_management.infrastructure import dtos

class DomainEvent(BaseModel, frozen=True):
    pass

class ProductCheckedout(DomainEvent):
    order_id: str
    destination: dtos.AddressDTO
    customer_details: dtos.CustomerDetailsDTO
    line_items: List[dtos.LineItemDTO]

class OrderPlaced(DomainEvent):
    order_id: str
    order_status: enums.OrderStatus
    customer_details: dtos.CustomerDetailsDTO
    shipping_details: dtos.ShippingDetailsDTO
    line_items: List[dtos.LineItemDTO]
    tax_details: List[str]
    tax_amount: dtos.MoneyDTO
    offer_details: List[str]
    total_discounts_fee: dtos.MoneyDTO
    final_amount: dtos.MoneyDTO

class OrderConfirmed(DomainEvent):
    order_id: str

class OrderShipped(DomainEvent):
    order_id: str

class OrderCancelled(DomainEvent):
    order_id: str

class OrderCompleted(DomainEvent):
    order_id: str

class PaymentApplied(DomainEvent):
    order_id: str
    amount: value_objects.Money
