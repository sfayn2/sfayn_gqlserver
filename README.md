# sfayn_gqlserver

[![Django CI](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml/badge.svg)](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml)

# Order Management API (DDD + GraphQL)

This service provides secure, JWT-authentication GraphQL APIs to manage customer orders using Domain-Drive Design (DDD) principles


## Work in Progress
This Project is currently under active development. Major changes are ongoing.


## Auth

All APIs require a **valid JWT** (eg. from Keycloak).
**No token -> No access.**

## API overview

GraphQL mutations/queries available:

### Checkout flow
- [`checkoutItems](./mutations/checkout_items.graphql)
- `addLineItem`
- `removeLineItem`
- `changeOrderQuantity`
- [`addCoupon`](./mutations/add_coupon.graphql)
- `listShippingOptions`
- [`selectShippingOption`](./mutations/selection_shipping_option.graphql)
- `listCustomerAddresses`
- [`changeDestination`](./mutations/change_destination.graphql)

### Order Lifecycle
- [`placeOrder` *(if draft order)*](./mutations/place_order.graphql)
- [`confirmOrder` *(if pending payment)*](./mutations/confirm_order.graphql)
- `cancelOrder` *(if pending/confirmed order)*
- [`markAsShipped` *(if confirmed order)*](./mutations/mark_as_shipped.graphql)
- `addShippingTrackingReference` *(if shipped order)*
- `markAsCompleted` *(if received)*

## Example flow
1. **User logs in via Idp (e.g Keycloak)**
2. **Frontend handles cart** (not API responsibility)
3. **Use GraphQL to checkout and build order**

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




