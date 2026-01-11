import uuid
from pydantic import BaseModel, root_validator, Field
from typing import Dict, Optional, List
from .base import IntegrationEvent
from ddd.order_management.application import dtos


class UserLoggedInIntegrationEvent(IntegrationEvent):
    data: dtos.UserContextDTO

