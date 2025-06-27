import uuid
from abc import ABC
from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
from ddd.order_management.domain import enums

class Query(BaseModel, frozen=True):
    pass

class ListShippingOptionsQuery(Query):
    order_id: str

class GetOrderQuery(Query):
    order_id: str

class ListCustomerAddressesQuery(Query):
    customer_id: str
