from __future__ import annotations
from abc import ABC, abstractmethod

class EmailServiceAbstract(ABC):
    @abstractmethod
    def send_email(self, message: str):
        raise NotImplementedError("Subclasses must implement this method")