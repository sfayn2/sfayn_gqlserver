import uuid
from abc import ABC
from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime
from ddd.order_management.domain import enums
from ddd.order_management.infrastructure import order_dtos

class Query(BaseModel, frozen=True):
    pass

class ShippingOptionsQuery(Query):
    order_id: str
