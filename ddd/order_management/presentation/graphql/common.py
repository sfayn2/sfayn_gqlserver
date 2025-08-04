import os
from ddd.order_management.domain import exceptions

def get_token_from_context(info):

    auth_header = info.context.META.get("HTTP_AUTHORIZATION")
    token_type = os.getenv("IDP_TOKEN_TYPE")

    if not token_type:
        raise exceptions.AccessControlException("Missing token type")

    if auth_header:
        if not auth_header.startswith(f"{self.token_type} "):
            raise exceptions.AccessControlException("Unsupported token type.")
        return auth_header.removeprefix(f"{self.token_type} ")

    return info.context.COOKIES.get("access_token")