# TenantOMSApi

[![Django CI](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml/badge.svg)](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml)

**TenantOMSAPi**  is a multi-tenant backend API for managing orders, shipments, etc built with Domain-Driven Design (DDD), GraphQL, and JWT-secured access.
it is IDP-agnostic, supports plan-based onboarding, and allows tenant-specific business configurations.


# Architecture Roles
* **SaaS Provider**: Owns SaasConfig, plans, permissions, integration, and core business rules.
* **Tenant**: Subscribes to SaaS plans, manages its own operational configuration via TenantConfig.
* **Vendor**: Operates under a tenant, uses authorized endpoints to manage orders, shipments, etc.

# Core Features
* **Multi-Tenant Isolation**: All operations scoped by tenant_id to ensure data separation
* **JWT Authentication (IDP-Agnostic)**: Works with any OIDC-compatible provider (e.g Keycloak)
* **Permission-Based API Access**: SaaS provider enables or restricts endpoints for each tenant via permissions.
* **Tenant Configuration**: Defines fees, refund policies, and other tenant-level behaviors.
* **Webhook Automation**: Tenants/B2B can automate order or shipment creation via shared-key secured webhook integration.
* **Event-Driven Integration**: Supports message-queue based integration (e.g. Redis Streams) for real-time synchronization between SaaS and tenant systems.
* **User Action Logging**: Trackes vendor actions (approveOrder, shipShipment, et) for audit and validations.


# Work in Progress
This Project is currently under active development. Major changes are ongoing.

## Typical Flow
1. Tenant subscribes to a SaaS provider plan (e.g Standard, Custom)
2. SaaS provider updates SaaSConfig -- Adds the subscribed tenant, its IDP issuer/public key, optional webhook shared key, etc.
3. Tenant sets up TenantConfig -- Defines its own operational settings (fees, refund rules, webhook URL, etc.)
4. Integration Setup
    * Tenant may automate order creation using webhooks.
    * For advanced real-time sync, they may connect via Redis Streams or another message queue
5. Vendors operation via TenantsOMSApi
* Use authenticated API endpoints to create orders, process shipments, refunds, and complete order flows.
* Access is enforece by tenant permissions defined in the SaaS plan.


# Configuration Overview
## SaaSConfig

Defines global SaaS-level settings, authorized tenants, and integration credentials.
```json
    {
        "idp": {
            "public_key": "92alSyFzFiPHT3oYDwjXAGXFAAAQGt1Eoaag5dw",
            "issuer": "http://idp.saasprovider.com/realms/tenant1",
            "audience": "AUD1",
            "algorith": "RS256",
        },
        "plan": ["standard"],
        "webhook_secret": "abc123secret",
    }
```

## TenantConfig

Defines tenant-specific business rules and integration endpoints
```json
    {
        "restocking_fee_percent": 10,
        "max_refund_amount": 500.0,
        "webhook_url": "https://tenant-a.app/webhook"
    }
```

## Contributing
Contributions welcome! Please open issues or submit pull requests




