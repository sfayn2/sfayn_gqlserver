import jwt

class JwtTokenHandler:
    def __init__(self, public_key: str, issuer: str, audience: str):
        self.public_key = public_key
        self.issuer = issuer
        self.audience = audience

    def decode(self, token: str) -> dict:

        jwks_client = PyJWKClient(self.public_key)
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        try:
            return jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                issuer=self.issuer,
                audience=self.audience
            )
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

