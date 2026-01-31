from typing import Any, Optional

#ports.ContextHeaderExtractorAbstract implementation for Django
class DjangoHeaderExtractor:
    def get_auth_header(self, context: Any) -> Optional[str]:
        return getattr(context, "META", {}).get("HTTP_AUTHORIZATION")
