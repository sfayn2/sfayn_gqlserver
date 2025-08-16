import uuid
from abc import ABC
from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
from ddd.order_management.domain import enums

class Query(BaseModel, frozen=True):
    token: str

class ListShippingOptionsQuery(Query):
    order_id: str

class GetOrderQuery(Query):
    order_id: str

class ListCustomerAddressesQuery(Query):
    customer_id: str
