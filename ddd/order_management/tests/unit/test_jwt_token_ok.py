import pytest, jwt
from datetime import datetime, timedelta
from ddd.order_management.infrastructure import (
    access_control1,
)

def test_jwt_token_ok(fake_rsa_keys, fake_jwt_valid_token):
    _, secret = fake_rsa_keys


    jwt_handler = access_control1.JwtTokenHandler(
        public_key=secret,
        issuer="https://issuer.test",
        audience="my-app",
        algorithm="RS256"
    )

    decoded = jwt_handler.decode(fake_jwt_valid_token, secret)
    assert decoded["sub"] == "user-1"
    assert decoded["iss"] == "https://issuer.test"
    assert decoded["tenant_id"] == "tenant_123"
    assert decoded["token_type"] == "Bearer"
    assert decoded["roles"] == ["vendor"]
