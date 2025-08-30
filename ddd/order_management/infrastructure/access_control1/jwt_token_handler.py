import jwt
from jwt import PyJWKClient
from typing import Optional

class JwtTokenHandler:
    def __init__(self, public_key: str, issuer: str, audience: str, algorithm: str):
        self.public_key = public_key
        self.issuer = issuer
        self.audience = audience
        self.algorithm = algorithm

    def decode(self, token: str, secret: Optional[str] = None) -> dict:

        if not secret:
            jwks_client = PyJWKClient(self.public_key)
            secret = jwks_client.get_signing_key_from_jwt(token).key

        try:
            return jwt.decode(
                token,
                secret,
                algorithms=[self.algorithm],
                issuer=self.issuer,
                audience=self.audience
            )
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

