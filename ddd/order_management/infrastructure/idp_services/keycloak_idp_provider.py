from __future__ import annotations
import requests
from ddd.order_management.application import dtos

class KeycloakIdPProvider:
    def __init__(self, token_url, client_id, client_secret):
        self.token_url = token_url
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

        return {
            "access_token" : data["access_token"],
            "refresh_token" : data["refresh_token"]
        }
