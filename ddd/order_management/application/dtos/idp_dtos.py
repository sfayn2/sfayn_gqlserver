import uuid
from pydantic import BaseModel, Field, AliasChoices, parse_obj_as

class IdPTokenDTO(BaseModel):
    access_token: str
    refresh_token: str
    #id_token: str
    #expires_in: int
    #scope: str
    #token_type: str