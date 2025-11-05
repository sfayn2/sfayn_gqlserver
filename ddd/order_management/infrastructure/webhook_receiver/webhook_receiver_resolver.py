from __future__ import annotations
from typing import Any
from datetime import datetime
from .easypost_webhook_receiver import EasyPostWebhookReceiver
from .github_webhook_receiver import GithubWebhookReceiver
from .wss_webhook_receiver import WssWebhookReceiver


class WebhookReceiverResolver:
    @staticmethod
    def resolve(config: dict):
        webhook_cfg = config.get("webhook")
        if webhook_cfg.get("provider") == "EASYPOST":
            return EasyPostWebhookReceiver(
                shared_secret=webhook_cfg.get("shared_secret"),
                max_age=webhook_cfg.get("max_age", None),
            )
        elif webhook_cfg.get("provider") == "GITHUB":
            return GithubWebhookReceiver(
                shared_secret=webhook_cfg.get("shared_secret")
            )
        elif webhook_cfg.get("provider") == "WSS":
            return WssWebhookReceiver(
                shared_secret=webhook_cfg.get("shared_secret")
            )