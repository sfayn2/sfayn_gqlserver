from __future__ import annotations
import uuid
from abc import ABC, abstractmethod

class UserAuthorizationSnapshotAbstract(ABC):

    @abstractmethod
    def get_all_users_auth(self) -> List[dtos.UserAuthorizationSnapshotDTO]:
        raise NotImplementedError("Subclasses must implement this method")

