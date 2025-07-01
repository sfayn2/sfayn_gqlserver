from __future__ import annotations
from abc import ABC, abstractmethod

class IdPProviderAbstract(ABC):
    @abstractmethod
    def get_token_by_code(self, code: str, redirect_uri: str) -> dtos.IdpTokenDTO:
        raise NotImplementedError("Subclasses must implement this method")

class LoginCallbackAbstract(ABC):

    def login_callback(code:str, redirect_uri: str) -> dtos.IdPTokenDTO:
        raise NotImplementedError("Subclasses must implement this method")
        