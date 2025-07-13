from ddd.order_management.domain import exceptions

def get_token_from_context(info):

    auth_header = info.context.META.get("HTTP_AUTHORIZATION")
    if auth_header:
        if not auth_header.startswith("Bearer "):
            raise exceptions.AccessControlException("Unsupported token type.")
        return auth_header.removeprefix("Bearer ")

    return info.context.COOKIES.get("access_token")