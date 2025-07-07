from __future__ import annotations
from abc import ABC, abstractmethod

class IdPLoginCallbackServiceAbstract(ABC):
    @abstractmethod
    def login_callback(self, code: str, redirect_uri: str) -> dtos.IdpTokenDTO:
        raise NotImplementedError("Subclasses must implement this method")

        