from pydantic import BaseModel, constr
from ddd.order_management.application import dtos
from .commands import Command

class EscalateReviewerCommand(Command):
    order_id: str
    reviewer: str
    comments: str

class ReviewOrderCommand(Command):
    order_id: str
    is_approved: bool
    comments: str