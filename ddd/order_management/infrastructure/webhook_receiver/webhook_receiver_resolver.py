from __future__ import annotations
from typing import Any
from datetime import datetime
from .easypost_webhook_receiver import EasyPostWebhookReceiver
from .github_webhook_receiver import GithubWebhookReceiver
from .wss_webhook_receiver import WssWebhookReceiver


class WebhookReceiverResolver:
    @staticmethod
    def resolve(cfg: dict):
        provider_name = cfg.get("provider_name")
        if provider_name == "EASYPOST":
            return EasyPostWebhookReceiver(
                shared_secret=cfg.get("shared_secret"),
                max_age=cfg.get("max_age", None),
            )
        elif provider_name == "GITHUB":
            return GithubWebhookReceiver(
                shared_secret=cfg.get("shared_secret")
            )
        elif provider_name == "WSS":
            return WssWebhookReceiver(
                shared_secret=cfg.get("shared_secret")
            )