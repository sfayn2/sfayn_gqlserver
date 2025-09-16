# LiteOMS

[![Django CI](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml/badge.svg)](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml)

# Lightweight, Integration-Focused Order Management API (DDD + GraphQL + JWT-secured)

A lightweight, multi-tenant **OMS** built with **Domain Driven Design (DDD)**. Focuses on workflow customization and integration rather than being a full-features all-in-one system

## Key Features
- Customizable Workflows - tenants can define sub-states and optional steps.
- JWT-secured, tenant-scoped APIs.
- Supports single-tenant or multi-tenant setups.
- Supports strong decoupling between bounded contexts (Snapshot Architecture).
- Integrates easily with external storefronts and fullfullment services.


## Work in Progress
This Project is currently under active development. Major changes are ongoing.


## Auth & Multi-Tenancy

- APIs are protected by **JWT access tokens**
- Use header: `Authorization: Bearer <your token>`
- Tokens must be issued by a trusted **IDP (e.g., Keycloak, Auth0, Firebase)**
- JWT **must include**:
    - `sub`: User id
    - `tenant_id`: Tenant Scope
    - `roles`: Customer or Vendor or Both



## Example flow
1. **Login** - User authenticates via IDP; optionally syncs to OMS.
2. **Place Order** - External storefornt calls OMS create order api with confirmed checkout order.
3. **Order Updates** - Vendor marks shipped, adds tracking, or completes order.
6. **Cancel / View** - Order in PENDING or CONFIRMED can be cancelled; order viewed via getOrder.


## Integration
* **External Storefronts**: Webhook reciever API; supports backend sync, CSV import or event-driven updates.
* **3rd-Party Services**: Fulfillment / 3PL updates via webhook APIs.


## Snapshots
* Local snapshots for read consistency and workflow decisions:
    * TenantWorkflowSnapshot
    * TenantRolemapSnapshot
    * FullfillmentSnapshot
    * UserAuthorizationSnapshot


## Contributing
Contributions welcome! Please open issues or submit pull requests




