
from typing import Any, Optional

#ports.ContextHeaderExtractorAbstract implementation for API Gateway

class APIGatewayHeaderExtractor:
    def get_auth_header(self, context: Any) -> Optional[str]:
        if not isinstance(context, dict): return None
        headers = context.get("request_event", {}).get("headers", {})
        return headers.get("Authorization") or headers.get("authorization")