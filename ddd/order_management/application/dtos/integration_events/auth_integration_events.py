import uuid
from pydantic import BaseModel, root_validator, Field
from typing import Dict, Optional, List
from .base import IntegrationEvent

class Identity(BaseModel):
    sub: str
    token_type: str
    tenant_id: str
    roles: List[str] = Field(default_factory=list)

class UserLoggedInIntegrationEvent(IntegrationEvent):
    data: Identity

