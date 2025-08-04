# sfayn_gqlserver

[![Django CI](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml/badge.svg)](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml)

# Order Management API (DDD + GraphQL)

This service provides secure, JWT-authentication GraphQL APIs to manage customer orders using Domain-Drive Design (DDD) principles


## Work in Progress
This Project is currently under active development. Major changes are ongoing.


## Auth

All APIs require a **valid JWT** (eg. from Keycloak).
Use header: `Authorization: Bearer <your token>`
**No token -> No access.**

## User Sync Requirement

if you're not using a shared [identity gateway](https://github.com/sfayn2/identity_gateway) to emit UserEventLoggedIn, you must sync the user manually to the Order system before calling GraphQL APIs.

## Tenant Scoping

Supports single-tenant or multi-tenant setups.
All JWTs must inlude a tenant_id claims.

* All orders, addresses, & line items are scoped by tenant_id
* Prevents cross-tenant data access or leakage
* Ensures isolation in multi-tenant Saas deployments

> Even in single-tenant mode, tenant_id is required to ensure consistency and future proofing.

## Example flow
1. **User logs in via Idp (e.g Keycloak)**
2. **Frontend handles cart** (not API responsibility)
3. **Use GraphQL to checkout and build order**

## API overview

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

- [`placeOrder` *(if draft order)*](./mutations/place_order.graphql)
- [`confirmOrder` *(if pending payment)*](./mutations/confirm_order.graphql)
- `cancelOrder` *(if pending/confirmed order)*
- [`markAsShipped` *(if confirmed order)*](./mutations/mark_as_shipped.graphql)
- `addShippingTrackingReference` *(if shipped order)*
- `markAsCompleted` *(if received)*


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




