import os, jwt
import traceback
from ddd.order_management.domain import exceptions

def get_token_from_context(info):

    ctx = info.context
    
    # CASE 1: Standard Django Request (On-Prem)
    if hasattr(ctx, "META"):
        auth_header = ctx.META.get("HTTP_AUTHORIZATION")
    
    # CASE 2: Lambda Event (AWS)
    elif isinstance(ctx, dict) and "request_event" in ctx:
        # Lambda Proxy integration puts headers in 'headers' key
        headers = ctx["request_event"].get("headers", {})
        # Headers in Lambda can be lowercase or capitalized depending on API Gateway version
        auth_header = headers.get("Authorization") or headers.get("authorization")
    
    else:
        raise exceptions.AccessControlException("Invalid context type")

    #auth_header = info.context.META.get("HTTP_AUTHORIZATION")
    #token_type = os.getenv("IDP_TOKEN_TYPE")
    token_type = "Bearer"

    if not token_type:
        raise exceptions.AccessControlException("Missing token type")

    if auth_header:
        if not auth_header.startswith(f"{token_type} "):
            raise exceptions.AccessControlException("Unsupported token type.")
        return auth_header.removeprefix(f"{token_type} ")

    return info.context.COOKIES.get("access_token")

def get_tenant_id(token: str):
    try:
        # to verify later in app handler
        unverified_payload = jwt.decode(
            token, options={"verify_signature": False }
        )
    except jwt.DecodeError:
        raise exceptions.AccessControlException("Invalid JWT format")

    tenant_id = unverified_payload.get("tenant_id")
    if not tenant_id:
        raise exceptions.AccessControlException("Missing tenant_id in token")

    return tenant_id