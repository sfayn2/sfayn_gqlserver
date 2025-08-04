# sfayn_gqlserver

[![Django CI](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml/badge.svg)](https://github.com/sfayn2/sfayn_gqlserver/actions/workflows/django.yml)

# Order Management API (DDD + GraphQL)

This service provides secure, JWT-authentication GraphQL APIs to manage customer orders using Domain-Drive Design (DDD) principles


## Work in Progress
This Project is currently under active development. Major changes are ongoing.


## Auth

All APIs require a **valid JWT** (eg. from Keycloak)
No token -> No access.

## API overview

GraphQL mutations/queries available:

### Checkout flow
- `checkoutItems`
- `addLineItem`
- `removeLineItem`
- `changeOrderQuantity`
- `addCoupon`
- `listShippingOptions`
- `selectShippingOption`
- `listCustomerAddresses`
- `changeDestination`

### Order Lifecycle
- `placeOrder` *(if draft order)*
- `confirmOrder` *(if pending payment)*
- `cancelOrder` *(if pending/confirmed order)*
- `markAsShipped` *(if confirmed order)*
- `addShippingTrackingReference` *(if shipped order)*
- `markAsCompleted` *(if received)*

## Example flow
1. **User logs in via Idp (e.g Keycloak)**
2. **Frontend handles cart** (not API responsibility)
3. **Use GraphQL to checkout and build order**

```graphql
   mutation {
  checkoutItems(input: {
    customerId: "c-234",
    vendorId: "v-234",
     address: {
    	street: "My street",
      city: "City1",
      state: "State1",
      postal: "12345",
      country: "Singapore"
    }
    productSkus:[
      {
        productSku: "T-SHIRT-L",
        orderQuantity: 10
      }
    ]
    
  }) {
    result {
      success
      message
    }
  }
}

mutation {
  placeOrder(input: {
    orderId: "ORD-AF29C5BA3036"
  }) {
    result {
      message
      success
    } 
  }
}

mutation {
  confirmOrder(input: {
    orderId: "ORD-FC8D8D9F",
    transactionId: "2L633961FY072164Y",
    method: "Paypal"
  }) {
result {
      message
      success
    } 

  }


  mutation {
  markAsShippedOrder(input: {
    orderId: "ORD-AF29C5BA3036",
}) {
    result {
      message
      success
    } 
  }
}
```

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




