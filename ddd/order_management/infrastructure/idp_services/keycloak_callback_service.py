from __future__ import annotations
import requests
from ddd.order_management.application import ports, dtos
from order_management import models as django_snapshots

class KeycloakLoginCallbackService(ports.IdPLoginCallbackServiceAbstract):

    def __init__(self, idp_provider, jwt_handler, role_map: dict[str, list[str]]):
        self.idp_provider = idp_provider
        self.jwt_handler = jwt_handler
        self.role_map = role_map

    def login_callback(self, code: str, redirect_uri: str) -> dtos.IdpTokenDTO:
        token_set = self.idp_provider.get_token_by_code(code, redirect_uri)
        access_token = token_set["access_token"]
        decoded = self.jwt_handler.decode(access_token)

        user_id = decoded["sub"]
        tenant_id = decoded.get("tenant_id")
        roles = decoded.get("realm_access", {}).get("roles", [])

        if not tenant_id:
            raise Exception("Missing tenant_id in token.")



        # Sync user auth
        django_snapshots.UserAuthorization.objects.filter(user_id=user_id).delete()
        for role in roles:
            permissions = self.role_map.get(role, [])
            for perm in permissions:
                scope = {"tenant_id": tenant_id}

                # customer_id or vendor_id
                if role == "customer":
                    scope["customer_id"] = user_id
                elif role == "vendor":
                    scope["vendor_id"] = user_id

                django_snapshots.UserAuthorization.objects.create(
                    user_id=user_id,
                    permission_code_name=perm,
                    scope=scope
                )

        #Sync customer
        if "customer" in roles:
            django_snapshots.CustomerDetailsSnapshot.objects.filter(user_id=user_id).delete()
            django_snapshots.CustomerDetailsSnapshot.objects.create(
                customer_id=user_id,
                user_id=user_id,
                first_name=decoded.get("given_name"),
                last_name=decoded.get("family_name"),
                email=decoded.get("email"),
                is_active=True
            )

        #Sync vendor
        #TODO?
        if "vendor" in roles:
            django_snapshots.VendorDetailsSnapshot.objects.filter(vendor_id=tenant_id).delete()
            django_snapshots.VendorDetailsSnapshot.objects.create(
                vendor_id=tenant_id,
                name=decoded.get("vendor_name"),
                country=decoded.get("vendor_country"),
                is_active=True
            )

        return dtos.IdPTokenDTO(
            access_token=access_token,
            refresh_token=token_set.get("refresh_token")
        )




#class KeycloakIdPCallbackService(ports.IdPCallbackServiceAbstract):
#    def __init__(self, base_url, realm, client_id, client_secret):
#        self.token_url = f"{base_url}/realms/{realm}/protocol/openid-connect/token"
#        self.client_id = client_id
#        self.client_secret = client_secret
#
#    def get_tokens(self, code: str, redirect_uri: str) -> dtos.IdPTokenDTO:
#        headers = {
#            "Content-Type": "application/x-www-form-urlencoded"
#        }
#        payload = {
#            "grant_type": "authorization_code",
#            "code": code,
#            "redirect_uri": redirect_uri,
#            "client_id": self.client_id,
#            "client_secret": self.client_secret
#        }
#
#        response = requests.post(self.token_url, data=payload, headers=headers)
#        response.raise_for_status()
#        data = response.json()
#
#        return dtos.IdPTokenDTO(
#            access_token=data["access_token"],
#            refresh_token=data.get("refresh_token", ""),
#            id_token=data.get("id_token", ""),
#            expires_in=data.get("expires_in", 0),
#            scope=data.get("scope", ""),
#            token_type=data.get("token_type", "Bearer")
#        )
#