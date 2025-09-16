import uuid
from pydantic import BaseModel, Field, AliasChoices, parse_obj_as
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Tuple
from ddd.order_management.domain import enums, value_objects
from ddd.order_management.application.dtos.dtos import MoneyDTO


class TenantWorkflowSnapshotDTO(BaseModel):
    tenant_id: str
    workflow: dict
    is_active: bool

