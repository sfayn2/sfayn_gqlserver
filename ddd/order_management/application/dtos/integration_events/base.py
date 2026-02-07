import uuid
from pydantic import BaseModel, root_validator, Field
from typing import Dict, Optional, List, Any
from .event_types import IntegrationEventType

class IntegrationEvent(BaseModel):
    event_type: IntegrationEventType
    data: Any
