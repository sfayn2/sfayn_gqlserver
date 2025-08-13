import pytest, os
from unittest.mock import patch, MagicMock
from ddd.order_management.presentation.webhook_apis import common
from ddd.order_management.infrastructure import webhook_signatures

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sfayn_gqlserver.settings')
import django
django.setup()


@pytest.fixture
def provider():
    return "wss"

@pytest.fixture
def tenant_id():
    return "tenant123"

@pytest.fixture
def valid_headers():
    return {
        "X-Wss-Signature": "validsignature",
        "X-Wss-Timestamp": "1223447890"
    }

@pytest.fixture
def valid_body():
    return b'{"product_id": "p-1234"}'

@patch.object(webhook_signatures, 'get_verifier_for')
def test_validate_webhook_success(mock_get_verifier_for, provider, tenant_id, valid_headers, valid_body):
    #verifier_mock = MagicMock()
    #verifier_mock.verify.return_value = True
    #monkeypatch.setattr(webhook_signatures, "get_verifier_for", lambda p, t, h: verifier_mock)
    mock_get_verifier_for.return_value.verify.return_value = True

    class DummyRequest:
        headers = valid_headers
        body = valid_body
    
    request = DummyRequest()

    payload = common.validate_webhook(provider, tenant_id, request)

    assert payload["product_id"] == "p-1234"
    assert payload["tenant_id"] == tenant_id

    #verifier_mock.verify.assert_called_once_with(valid_headers, valid_body)
    mock_get_verifier_for.return_value.verify.assert_called_once_with(request.headers, request.body)

#def test_validate_webhook_invalid_signature(monkeypatch, provider, tenant_id, valid_headers, valid_body):
#    verifier_mock = MagicMock()
#    verifier_mock.verify.return_value = True
#    monkeypatch.setattr(webhook_signatures, "get_verifier_for", lambda p, t, h: verifier_mock)
#
#    class DummyRequest:
#        headers = valid_headers
#        body = valid_body
#    
#    request = DummyRequest()
#
#    with pytest.raises(Exception, match="Invalid signature"):
#        common.validate_webhook(provider, tenant_id, request)
