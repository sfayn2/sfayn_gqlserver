from __future__ import annotations
import os
from typing import Optional
from ddd.order_management.infrastructure import webhook_signatures

def get_verifier_for(headers: dict) -> Optional[ports.WebhookSignatureVerifier]

    if "X-WSS-Signature" in headers:
        return webhook_signatures.WSSSignatureVerifier(shared_secret=os.get_env("WH_WSS_SECRET")) 
    
    if "X-Hub-Signature-256" in headers:
        return webhook_signatures.GithubSignatureVerifier(secret=os.get_env("WH_HUB_SECRET"))