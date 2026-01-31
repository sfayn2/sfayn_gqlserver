import pytest, jwt
from datetime import datetime, timedelta
from ddd.order_management.infrastructure import (
    access_control1,
)

@pytest.mark.django_db
def test_jwt_token_expired(fake_rsa_keys, fake_jwt_expired_token):
    _, secret = fake_rsa_keys


    jwt_handler = access_control1.JwtTokenHandler(
        public_key=secret,
        issuer="https://issuer.test",
        audience="my-app",
        algorithm="RS256"
    )

    with pytest.raises(Exception) as exc_info:
        decoded = jwt_handler.decode(fake_jwt_expired_token, secret)

    assert str(exc_info.value) == "Token expired"