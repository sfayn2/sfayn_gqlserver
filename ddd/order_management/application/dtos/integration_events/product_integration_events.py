import uuid
from pydantic import BaseModel, root_validator, Field
from typing import Dict, Optional, List

class ProductIntegrationEvent(BaseModel):
    event_type: str
    tenant_id: str
    data: dtos.ProductSnapshotDTO


