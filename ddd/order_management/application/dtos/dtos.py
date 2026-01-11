import uuid
from pydantic import BaseModel, Field, AliasChoices, parse_obj_as
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Tuple, Dict, Any
from ddd.order_management.domain import enums, value_objects


class UserContextDTO(BaseModel):
    sub: str
    token_type: str
    tenant_id: str
    roles: List[str] = Field(default_factory=list)


class UserActionDTO(BaseModel):
    order_id: str
    action: str
    performed_by: str
    user_input: Dict[str, Any]





# SaasConfig / TenantConfig related DTOs
class CreateShipmentConfigDTO(BaseModel):
    # all shipments tracker webhook / create shipments
    provider: str
    api_key: str
    endpoint: str

class WebhookReceiverConfigDTO(BaseModel):
    provider: str
    shared_secret: str
    max_age_seconds: Optional[int] = None
