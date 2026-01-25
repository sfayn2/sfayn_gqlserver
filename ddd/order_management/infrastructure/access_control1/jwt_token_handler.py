import jwt, os
from jwt import PyJWKClient
from typing import Optional

class JwtTokenHandlerException(Exception):
    """Unified exception for JWT Token Handler failures."""
    pass

class JwtTokenHandler:
    def __init__(self, public_key: str, issuer: str, audience: str, algorithm: str):
        self.public_key = public_key
        self.issuer = issuer
        self.audience = audience
        self.algorithm = algorithm

    def decode(self, token: str, secret: Optional[str] = None) -> dict:

        # 1. Check for the Fake Switch (LocalStack/Dev Mode)
        # Setting SKIP_JWT_VERIFY="true" allows offline decoding
        if os.environ.get("SKIP_JWT_VERIFY") == "true":
            try:
                # We decode without verification to avoid the JWKS network call
                decoded = jwt.decode(token, options={"verify_signature": False})
                print("WARNING: SKIP_JWT_VERIFY is enabled. Token not verified.", decoded)

                return decoded
            except jwt.InvalidTokenError as e:
                raise JwtTokenHandlerException(f"Invalid token format during skip-verify: {str(e)}")

        if not secret:
            try:
                jwks_client = PyJWKClient(self.public_key, cache_keys=True, lifespan=3600)
                secret = jwks_client.get_signing_key_from_jwt(token).key
            except Exception as e:
                raise JwtTokenHandlerException(f"Failed to retrieve JWKS key from url {self.public_key}: {str(e)}")

        try:
            return jwt.decode(
                token,
                secret,
                algorithms=[self.algorithm],
                issuer=self.issuer,
                audience=self.audience
            )
        except jwt.ExpiredSignatureError:
            raise JwtTokenHandlerException("Token expired")
        except jwt.InvalidIssuerError:
            raise JwtTokenHandlerException(f"Invalid issuer. Expected: {self.issuer}")
        except jwt.InvalidAudienceError:
            raise JwtTokenHandlerException(f"Invalid audience. Expected: {self.audience}")
        except jwt.InvalidTokenError as e:
            # Catch-all for signature mismatches or malformed claims
            raise JwtTokenHandlerException(f"Invalid token: {str(e)}")
