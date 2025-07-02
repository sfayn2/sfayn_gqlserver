from __future__ import annotations
import requests
from ddd.order_management.application import ports, dtos


class KeycloakIdPCallbackService(ports.IdPCallbackServiceAbstract):
    def __init__(self, base_url, realm, client_id, client_secret):
        self.token_url = f"{base_url}/realms/{realm}/protocol/openid-connect/token"
        self.client_id = client_id
        self.client_secret = client_secret

    def get_tokens(self, code: str, redirect_uri: str) -> dtos.IdPTokenDTO:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        response = requests.post(self.token_url, data=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        return dtos.IdPTokenDTO(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token", ""),
            id_token=data.get("id_token", ""),
            expires_in=data.get("expires_in", 0),
            scope=data.get("scope", ""),
            token_type=data.get("token_type", "Bearer")
        )
