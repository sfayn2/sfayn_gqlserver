from __future__ import annotations
from typing import Protocol

class EmailSenderAbstract(Protocol):
    @abstractmethod
    def send_email(self, message: str): ...