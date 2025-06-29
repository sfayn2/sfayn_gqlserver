import os
import requests
import base64
import json
from dotenv import load_dotenv
import jwt
from jwt import PyJWKClient

load_dotenv()

# === config
CLIENT_ID = os.getenv("CLIENT_ID")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


# ====== token request ===
token_endpoint = f"http://localhost:8080/realms/CustomerRealm/protocol/openid-connect/token"
jwks_uri = "http://localhost:8080/realms/CustomerRealm/protocol/openid-connect/certs"
issuer = "http://localhost:8080/realms/CustomerRealm"

data = {
    "grant_type": "password",
    "client_id": CLIENT_ID,
    "username": USERNAME,
    "password": PASSWORD,
}

response = requests.post(token_endpoint, data=data)

if response.status_code != 200:
    print("failed to get token")
    print(response.text)
    exit(1)

tokens = response.json()
access_token = tokens["access_token"]
id_token = tokens.get("id_token", "<none>")
print(f"access token received!")

jwks_client = PyJWKClient(jwks_uri)
signing_key = jwks_client.get_signing_key_from_jwt(access_token)

decoded = jwt.decode(
    access_token,
    signing_key.key,
    algorithms=["RS256"],
    issuer=issuer,
)

print("decoded access token payload:")
print(decoded)