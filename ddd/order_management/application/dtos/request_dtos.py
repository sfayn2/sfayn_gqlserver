from pydantic import BaseModel, Field, AliasChoices, parse_obj_as

# define security context
class RequestContextDTO(BaseModel):
    token: str
    tenant_id: str