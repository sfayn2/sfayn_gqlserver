from __future__ import annotations
import hmac, hashlib, time
from typing import Mapping
# Assuming 'DomainClock' provides a compatible 'now()' method that returns a datetime object
# from ddd.order_management.domain.services import DomainClock 
# (You will need to ensure DomainClock is available or replace with a standard library approach)

# WebhookReceiverAbstract
class EasyPostWebhookReceiver:
    """
    Verifies the authenticity and integrity of EasyPost webhooks using HMAC-SHA256 V2 method.
    """
    def __init__(self, shared_secret: str, max_age_seconds: int = 300):
        # The secret is provided when creating the webhook in the EasyPost dashboard
        self.secret = shared_secret.encode('utf-8')
        self.max_age = max_age_seconds

    def verify(self, headers: Mapping[str, str], raw_body: bytes, request_path: str) -> bool:
        """
        Main verification method.
        
        Args:
            headers: The dictionary of request headers. Header names are case-insensitive in HTTP.
            raw_body: The raw bytes of the request body (crucial for correct hashing).
            request_path: The URL path of your endpoint (e.g., '/webhook/easypost').

        Returns:
            bool: True if the signature is valid and the request is fresh, False otherwise.
        """
        # EasyPost uses specific header names:
        signature_header_v2 = headers.get("X-Hmac-Signature-V2", headers.get("x-hmac-signature-v2", ""))
        timestamp_header = headers.get("X-Timestamp", headers.get("x-timestamp", "")) # RFC 2822 format

        if not signature_header_v2 or not timestamp_header:
            return False

        # 1. Check timestamp freshness (replay attack protection)
        if not self._is_timestamp_fresh(timestamp_header):
            return False

        # 2. Recompute the expected signature
        expected_signature = self._generate_signature(timestamp_header, request_path, raw_body)

        # 3. Securely compare the expected signature with the received one
        # Note: EasyPost signature is a lowercase hex string
        return hmac.compare_digest(expected_signature, signature_header_v2.lower())

    def _is_timestamp_fresh(self, timestamp_str: str) -> bool:
        """Checks if the timestamp is within the acceptable time window."""
        try:
            # EasyPost uses RFC 2822 timestamp format, which is standard
            # We compare against the current system time
            now_ts = time.time()
            event_ts = time.mktime(time.strptime(timestamp_str, "%a, %d %b %Y %H:%M:%S %z"))

            if abs(now_ts - event_ts) >= self.max_age:
                return False
        except ValueError:
            # Handle invalid timestamp format
            return False
        return True

    def _generate_signature(self, timestamp: str, path: str, body: bytes) -> str:
        """Generates the expected HMAC-SHA256 signature."""
        # The string-to-sign is created by concatenating timestamp, path, and body
        string_to_sign = f"{timestamp}{path}".encode('utf-8') + body

        # Calculate HMAC SHA-256 hash
        hashed = hmac.new(self.secret, string_to_sign, hashlib.sha256).hexdigest()
        return hashed
