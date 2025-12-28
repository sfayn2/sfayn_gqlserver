# TenantOMSApi

[![Django CI](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml/badge.svg)](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml)

**TenantOMSAPi**  is a multi-tenant backend API for managing orders, shipments, etc built with Domain-Driven Design (DDD), GraphQL, and JWT-secured access.
it is IDP-agnostic, supports plan-based onboarding, and allows tenant-specific business configurations while remaining deployable to AWS Serverless infrastructure.


# Architecture Roles
* **SaaS Provider**: Owns SaasConfig, plans, permissions, integration, and core business rules.
* **Tenant**: Subscribes to SaaS plans, manages its own operational configuration via TenantConfig.
* **Vendor**: Operates under a tenant, uses authorized endpoints to manage orders, shipments, etc.

# Core Features
* **Multi-Tenant Isolation**: All operations scoped by tenant_id to ensure data separation
* **JWT Authentication (IDP-Agnostic)**: Works with any OIDC-compatible provider (e.g Keycloak, AWS Cognito, etc.)
* **Permission-Based API Access**: SaaS provider enables or restricts endpoints for each tenant via permissions.
* **Tenant Configuration**: Defines fees, refund policies, and other tenant-level behaviors.
* **Webhook Automation**: Tenants/B2B can automate order or shipment creation via shared-key secured webhook integration.
* **Event-Driven Integration**: Supports message-queue based integration (e.g. Redis Streams, AWS EventBridge) for real-time synchronization between SaaS and tenant systems.
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
            "public_key": "xyzckawe23@#%#$sdfgsdfgdfgfgdfgkjwelrt",
            "issuer": "http://idp.saasprovider.com/realms/t1",
            "audience": "AUD1",
            "algorithm": "RS256",
        },
        "webhooks": {
            "shipment_tracker": {
                "provider": "easypost",
                "shared_secret": "secret123",
                "max_age_seconds": 3000,
                "tracking_reference_jmespath": "result.tracking_code || data.tracking_code",
            },
            "add_order": {
                "provider": "wss",
                "shared_secret": "secret234",
                "max_age_seconds": 3000,
            }
        },
        "create_shipment_api": {
            "provider": "easypost",
            "api_key": "api key",
            "endpoint": "https://endpoint.dev",
        }
    }
```

## TenantConfig

Defines tenant-specific business rules and integration endpoints
```json
    {
        "restocking_fee_percent": 10,
        "max_refund_amount": 500.0,
    }
```
# Deployment Architecture (AWS Serverless)
## High-Level Overview

TenantOMSApi is fully deployable as a serverless system using AWS managed services:
<img width="1099" height="955" alt="image" src="https://github.com/user-attachments/assets/c8ee3016-f717-4ed7-b439-ef2f39399ad2" />


## Contributing
Contributions welcome! Please open issues or submit pull requests




