# sfayn_gqlserver

[![Django CI](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml/badge.svg)](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml)

# Order Management API (DDD + GraphQL + JWT-secured)

A modular, multi-tenant **Order Management System** built with **Domain Driven Design (DDD)**. Designed to plug into any product catalog, vendor registry, or identity provider.

## Key Features
- Full checkout + order lifecycle
- JWT-secured, tenant-scope APIs
- Supports single-tenant or multi-tenant setups.
- Supports strong decoupling between bounded contexts (Snapshot Architecture)
- Prevents cross-tenant data access or leakage
- Ensures isolation in multi-tenant Saas deployments
- Works out of the box with our [catalog](https://github.com/sfayn2/catalog_service), [vendor registry](https://github.com/sfayn2/vendor_registry), [identify gateway](https://github.com/sfayn2/identity_gateway), & [webhook sender service](https://github.com/sfayn2/webhook_sender_service)
- Supports snapshot sync from external systems or manual CSV import (by request)


> OMS-agnostic: Can integrate with any system via snapshot sync and available webhooks APIs.


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

- if using our [IDP Gateway](https://github.com/sfayn2/identity_gateway) can emit UserEventLoggedInEvent, users are **auto-synced**
- else, frontend must call [syncUser]() manually to the OMS before calling GraphQL Checkout/Order lifecycle flow APIs.


## Example flow
1. **User Login**
* Frontend logs in via IDP (e.g Keycloak)
* Retrieve JWT
* Optionally call syncUser if not using out of the box [IDP gateway](https://github.com/sfayn2/identity_gateway)
2. **Cart Management**
* Frontend handles cart UX
* Allow user to fill in customer details + address, When ready to checkout, call [checkoutItems](./mutations/checkout_items.graphql)
3. **Checkout**
* Add more items[addLineItems](./mutations/add_line_items.graphql), [removeLineItems](./mutations/remove_line_items.graphql), or Change product order quantity [changeOrderQuantity](./mutations/change_order_quantity.graphql).
* Fetch addresses ([listCustomerAddresses](./mutations/list_customer_addresses.graphql))
* Select destination from addresses (or provide new address) via [changeDestination](./mutations/change_destination.graphql).
* Apply coupons via  [addCoupon](./mutations/add_coupon.graphql))
* Select shipping via [listShippingOption](./mutations/list_shipping_option.graphql) & [selectShippingOption](./mutations/selection_shipping_option.graphql)
4. **Place Order**
* Call [placeOrder](./mutations/place_order.graphql) to persist the order
5. **Payment + Fulfillment**
* After successfull payment, call [confirmOrder](./mutations/confirm_order.graphql)
* Vendor then updates order via:
    * [markAsShipped](./mutations/mark_as_shipped.graphql)
    * [addShippingTrackingReference](./mutations/add_shipping_tracking_reference.graphql)
    * [markAsCompleted](./mutations/mark_as_completed.graphql)
6. **Cancel Order**
* Orders in PENDING or CONFIRMED can be cancelled via [cancelOrder](./mutations/cancel_order.graphql)
7. **View Order Details**
* View Customer Order [getOrder](./mutations/get_order.graphql)

## Snapshot Strategy

The OMS relies on local snapshot models for product, vendor, offer, shipping, and user-related data. These  snapshots are used for read consistency and calculated decisions at the time of checkout or order placement.

### Support snapshots
- VendorProductSnapshot
- VendorDetailsSnapshot
- VendorCoupon
- VendorOffersSnapshot
- VendorShippingOptionsSnapshot
- CustomerDetailsSnapshot
- CustomerAddressSnapshot
- UserAuthorizationSnapshot

> `CustomerDetailsSnapshot` and `CustomerAddressesSnapshot` can also be populated at the time of checkout, so external sync is optional.


### Integration Strategies

1. **Seamless with our Ecosystem**
    This OMS API works out of the box with our:
    - [catalog](https://github.com/sfayn2/catalog_service)
    - [vendor registry](https://github.com/sfayn2/vendor_registry)
    - [webhook sender service](https://github.com/sfayn2/webhook_sender_service)
    - [identify gateway](https://github.com/sfayn2/identity_gateway)

Snapshots are automatically updated via internal event sync. No extra integration is required.

2. **External System Integration**
if you're using an external product or vendor catalog:
    - You must provide your own snapshot sync logic per tenant.
    - Supported strategies:
        - Custom backend sync service (by request)
        - Manual CSV import (see below)
        - Event-driven updates (using existing OMS webhook APIs handler)

### Manual Snapshot Import (by request)
For simpler onboarding, we support manual snapshot import via `.csv` upload on request.

> Ask us for CSV template formats to start importing your data manually.

### Webhooks & Eventing Guidance
To keep local snapshots consistent

- Emit Webhook events from your upstream systems whenever relevant data changes and trigger OMS snapshot sync APIs by calling our webhook endpoints, which handle the updates internally.

    > CustomerDetailsSnapshot and CustomerAddressesSnapshot can be synced from (Optional):
        - Manual frontend sync during checkoutItems or changeDestination

    > Ask us to setup webhook support for your signature calculation method. Also shared secret will be issued for secure integration

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




