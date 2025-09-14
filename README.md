# sfayn_gqlserver

[![Django CI](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml/badge.svg)](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml)

# Lightweight, Integration-Focused Order Management API (DDD + GraphQL + JWT-secured)

A lightweight, multi-tenant **OMS** built with **Domain Driven Design (DDD)**. Focuses on workflow customization and easy integration with external storefronts, or fullfillment services.

## Key Features
- Customizable Workflows - tenants can define sub-states and optional steps.
- JWT-secured APIs - tenant-scoped access control
- Supports single-tenant or multi-tenant setups.
- Supports strong decoupling between bounded contexts (Snapshot Architecture)
- Prevents cross-tenant data access or leakage
- Ensures isolation in multi-tenant Saas deployments
- Integrate with external storefronts, fullfillment system via webhook APIs


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
1. **User Login**
* Frontend logs in via IDP (e.g Keycloak)
* Retrieve JWT
* Optionally call syncUser if not using out of the box [identity gateway](https://github.com/sfayn2/identity_gateway)
2. **Place Order in OMS**
* Storefront callse placeOrder with finalized order data from checkout [checkout cart]()
* OMS persists order and line items.
3. **Order Lifecycle Updates**
* Vendor then updates order via:
    * [markAsShipped](./sample_mutations/mark_as_shipped.graphql)
    * [addShippingTrackingReference](./sample_mutations/add_shipping_tracking_reference.graphql)
    * [markAsCompleted](./sample_mutations/mark_as_completed.graphql)
6. **Cancel Order**
* Orders in PENDING or CONFIRMED can be cancelled via [cancelOrder](./sample_mutations/cancel_order.graphql)
7. **View Order Details**
* View Customer Order [getOrder](./sample_mutations/get_order.graphql)

## Snapshot Strategy

The OMS relies on local snapshot models for tenant, vendor, and user-related data.

### Support snapshots
- TenantWorkflowSnapshot
- TenantRolemapSnapshot
- FullfillmentSnapshot?
- UserAuthorizationSnapshot


### Integration Strategies

1. **Seamless with our Ecosystem**
    This OMS API works out of the box with our:
    - [checkout_cart](https://github.com/sfayn2/checkout_cart)
    - [tenant registry](https://github.com/sfayn2/tenant_registry)
    - [webhook sender service](https://github.com/sfayn2/webhook_sender_service)
    - [identity gateway](https://github.com/sfayn2/identity_gateway)

Snapshots are automatically updated via internal event sync. No extra integration is required.

2. **External System Integration**
if you're using an external storefront, orders can be synced via:
    - Supported strategies:
        - Custom backend sync service (by request)
        - Manual CSV import (see below)
        - Event-driven updates (using existing OMS webhook receiver APIs handler)

3. **3rd Party Integration**
    - Fullfillment / 3PL services

### Manual Snapshot / Order Import (by request)
For simpler onboarding, we support manual snapshot import via `.csv` upload on request.

> Ask us for CSV template formats to start importing your data manually.

### Webhooks & Eventing Guidance
To keep local snapshots consistent

- Emit Webhook events from your upstream systems whenever relevant data changes and trigger OMS snapshot sync APIs by calling our webhook endpoints, which handle the updates internally.

    > Ask us to setup webhook support for your signature calculation method. Also shared secret will be issued for secure integration


## Contributing
Contributions welcome! Please open issues or submit pull requests




