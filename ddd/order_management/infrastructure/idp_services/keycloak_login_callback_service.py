from __future__ import annotations
import os
from ddd.order_management.application import ports
from ddd.order_management.infrastructure import idp_services


class KeycloakLoginCallbackService(ports.LoginCallbackAbstract):

    def login_callback(self, code:str, redirect_uri: str) -> dtos.IdPTokenDTO:
        
        idp_provider = idp_services.KeycloakIdPProvider(
            base_url=os.getenv("KEYCLOAK_BASE_URL"),
            realm=os.getenv("KEYCLOAK_REALM"),
            client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
            client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET")
        )

        token_set = idp_provider.get_token_by_code(code, redirect_uri)

        return token_set

