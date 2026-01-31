from typing import Optional
from ddd.order_management.domain import exceptions
from ddd.order_management.application import ports, dtos

class GraphqlContext:
    saas_lookup_service: Optional[ports.LookupServiceAbstract] = None
    header_extractor: Optional[ports.ContextHeaderExtractorAbstract] = None


    @classmethod
    def configure(cls, saas_lookup_service: ports.LookupServiceAbstract, header_extractor: ports.ContextHeaderExtractorAbstract) -> None:
        cls.saas_lookup_service = saas_lookup_service
        cls.header_extractor = header_extractor



def get_token_from_context(info, tenant_id) -> str:

    # 1. Strategy-based extraction (Clean & Fast)
    if not GraphqlContext.header_extractor:
        raise exceptions.AccessControlException("Context extractor not configured")
    
    auth_header = GraphqlContext.header_extractor.get_auth_header(info.context)
    if not auth_header:
        raise exceptions.AccessControlException("Authorization header not found in context")

    # Determine tenant ID from the request to fetch correct token type
    if GraphqlContext.saas_lookup_service is None:
        raise exceptions.AccessControlException("SaaS lookup service not configured")
    
    config_source = GraphqlContext.saas_lookup_service.get_tenant_config(tenant_id)

    if not config_source.configs:
        # 2. Raise a specific custom exception instead of a generic ValueError
        raise Exception(f"No configuration found for tenant_id: {tenant_id} in SaaS lookups.")

    token_type = config_source.configs.get("idp", {}).get("token_type", "Bearer")
    

    #token_type = "Bearer"
    if auth_header:
        if not auth_header.startswith(f"{token_type} "):
            raise exceptions.AccessControlException("Unsupported token type.")
        return auth_header.removeprefix(f"{token_type} ")

    return info.context.COOKIES.get("access_token")




def get_request_context(info, **input_data) -> dtos.RequestContextDTO:
    """
    Common factory to extract tenant_id and token, returning a 
    validated RequestContextDTO.
    """
    tenant_id = input_data.get("tenant_id")
    if not tenant_id:
        # Extra safety check if a developer forgets required=True in GraphQL
        raise Exception("tenant_id is required to establish request context.")
        
    token = get_token_from_context(info, tenant_id=tenant_id)

    return dtos.RequestContextDTO(
        token=token,
        tenant_id=tenant_id
    )

