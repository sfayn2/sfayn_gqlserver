from __future__ import annotations
from abc import ABC, abstractmethod

class IdPCallbackServiceAbstract(ABC):
    @abstractmethod
    def get_tokens(self, code: str, redirect_uri: str) -> dtos.IdpTokenDTO:
        raise NotImplementedError("Subclasses must implement this method")

        