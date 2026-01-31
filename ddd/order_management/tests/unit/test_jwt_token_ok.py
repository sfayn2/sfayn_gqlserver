import pytest, jwt
from datetime import datetime, timedelta
from ddd.order_management.infrastructure import (
    access_control1,
)

@pytest.mark.django_db
def test_jwt_token_ok(fake_rsa_keys, fake_jwt_valid_token):
    _, secret = fake_rsa_keys


    jwt_handler = access_control1.JwtTokenHandler(
        public_key=secret,
        issuer="https://issuer.test",
        audience="my-app",
        algorithm="RS256"
    )

    decoded = jwt_handler.decode(fake_jwt_valid_token, secret)
    assert decoded["sub"] == "7494d733-5030-4979-8aa9-637571f533a7"
    assert decoded["iss"] == "https://issuer.test"
    assert "tenant_123" in decoded["organization"]
    assert decoded["typ"] == "Bearer"
    assert decoded["roles"] == ["vendor"]
