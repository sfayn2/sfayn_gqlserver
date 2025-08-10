from __future__ import annotations
import os
from typing import Optional
from ddd.order_management.infrastructure import webhook_signatures

def get_verifier_for(provider: str, tenant_id: str, headers: dict) -> Optional[ports.WebhookSignatureVerifier]:

    provider = provider.lower()
    secret = os.get_env(f"WS_SECRET_{tenant_id}")
    if not secret:
        return None

    if provider == "wss":
        return webhook_signatures.WSSSignatureVerifier(shared_secret=secret) 
    
    if provider == "github":
        return webhook_signatures.GithubSignatureVerifier(secret=secret)

    return None