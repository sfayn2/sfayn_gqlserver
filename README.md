# sfayn_gqlserver

[![Django CI](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml/badge.svg)](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml)

# Order Management API (DDD + GraphQL + JWT-secured)

A modular, single multi-tenant **Order Management System** built with **Domain Driven Design (DDD)**. Designed to plug into any product catalog, vendor registry, or identity provider.

## Key Features
- Full checkout + order lifecycle
- JWT-secured, tenant-scope APIs
- Supports single-tenant or multi-tenant setups.
- Supports strong decoupling between bounded contexts (Snapshot Architecture)
- Prevents cross-tenant data access or leakage
- Ensures isolation in multi-tenant Saas deployments
- Works out of the box with our [catalog](https://github.com/sfayn2/catalog_service), [vendor registry](https://github.com/sfayn2/vendor_registry), & [identify gateway](https://github.com/sfayn2/identity_gateway)
- Supports snapshot sync from external systems or manual CSV import (by request)


> OMS-agnostic: Can integrate with any system via snapshot sync.


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


## User Sync Requirement

- if using our [IDP Gateway](https://github.com/sfayn2/identity_gateway) to emit UserEventLoggedIn, users are **auto-synced**
- else, frontend must call [syncUser]() manually to the OMS before calling GraphQL Checkout/Order lifecycle flow APIs.




## GraphQL API overview

GraphQL mutations/queries available:

### Checkout flow

> Run these APIs after the frontend cart is prepared:

- [`checkoutItems](./mutations/checkout_items.graphql)
- `addLineItem`, `removeLineItem`, `changeOrderQuantity`
- [`addCoupon`](./mutations/add_coupon.graphql)
- `listCustomerAddresses`
- [`changeDestination`](./mutations/change_destination.graphql)
- `listShippingOptions`
- [`selectShippingOption`](./mutations/selection_shipping_option.graphql)

### Order Lifecycle
> Once ready, move the order through its lifecycle 

- [`placeOrder`](./mutations/place_order.graphql)
- [`confirmOrder`](./mutations/confirm_order.graphql)
- `cancelOrder`
- [`markAsShipped`](./mutations/mark_as_shipped.graphql)
- `addShippingTrackingReference`
- `markAsCompleted`

## Example flow
1. **User Login**
* Frontend logs in via IDP (e.g Keycloak)
* Retrieve JWT
* Optionally call syncUser if not using out of the box IDP gateway
2. **Cart Management**
* Frontend handles cart UX
* When ready to checkout, call [checkoutItems]() and [addLineItems]().
3. **Checkout**
* Fetch addresses ([listCustomerAddresses]()) or provide new address.
* Select destination via [changeDestination]()
* Apply coupons via  [addCoupon]()
* Select shipping via [listShippingOption]() & [selectShippingOption]()
4. **Place Order**
* Call placeOrder to persist the order
5. **Payment + Fulfillment
* After successfull payment, call [confirmOrder]()
* Vendor then updates order via:
    * markAsShipped
    * addShippingTrackingReference
    * markAsCompleted
6. **Cancel Order**
* Orders in PENDING or CONFIRMED can be cancelled via [cancelOrder]()

## Snapshot Strategy

The OMS relies on local snapshot models for product, vendor, offer, shipping, and user-related data. These  snapshots are used for read consistency and calculated decisions at the time of checkout or order placement.

### Support snapshots
- ProductSnapshot
- VendorDetailsSnapshot
- VendorsCoupon
- VendorOffersSnapshot
- VendorShippingOptionsSnapshot
- CustomerDetailsSnapshot
- CustomerAddressSnap

> `CustomerDetailsSnapshot` and `CustomerAddressesSnapshot` can also be populated at the time of checkout, so external sync is optional.

### Integration Strategies

1. **Seamless with our Ecosystem**
This OMS API works out of the box with our:
- Product Catalog
- Vendor Registry (Offers & Shipping Options)

Snapshots are automatically updated via internal event sync. No extra integration is required.

2. **External System Integration**
if you're using an external product or vendor catalog:
- You must provide your own snapshot sync logic per tenant.
- Supported strategies:
    - Custom backend sync service (by request)
    - Event-driven updates?
    - Frontend-initiated snapshot sync (e.g after login)
    - Manual CSV import (see below)

3. **Manual Snapshot Import (by request)**
For simpler onboarding or non-technical users, we support manual snapshot import via `.csv` upload on request.
- Supports:
    - ProductSnapshot
    - VendorDetailsSnapshot
    - VendorOffersSnapshot
    - VendorsShippingOption
    - VendorsCoupon

> Ask us for CSV template formats to start importing your data manually.

### Webhooks & Eventing Guidance
To keep local snapshots consistent;

- Emit change events from your systems:
    - ProductUpdatedEvent
    - TBD
- Register a webhook target with our API per tenant (Coming soon)

### User Snapshot Sync (Optional)
- CustomerDetailsSnapshot and CustomerAddresses can be synced from:
    - IDP gateway login callback (e.g. Keycloak)
    - Manual frontend sync after login (TBD)
    - Or directly populated during checkout  (recommended for minimal setup)

## Installation 
```
cd /home/{username}/sfayn_gqlserver
pip install -r requirements
```

## How to run development server? 
```
python manage.py runserver 0.0.0.0:4000
```


### Help

Need help? Open an issue in: [ISSUES](https://github.com/sfayn2/sfayn_gqlserver/issues)


### Contributing
Want to improve and add feature? Fork the repo, add your changes and send a pull request.




