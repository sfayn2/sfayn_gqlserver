import uuid
from pydantic import BaseModel, root_validator, Field
from typing import Dict, Optional, List, Any

class IntegrationEvent(BaseModel):
    event_type: str
    data: Any
