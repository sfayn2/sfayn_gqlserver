class InvalidOrderOperation(Exception):
    pass

class MoneyException(InvalidOrderOperation):
    pass

class AddressException(InvalidOrderOperation):
    pass

class CouponException(InvalidOrderOperation):
    pass

class CustomerDetailsException(InvalidOrderOperation):
    pass

class OfferStrategyException(InvalidOrderOperation):
    pass

class PackageException(InvalidOrderOperation):
    pass

class PaymentDetailsException(InvalidOrderOperation):
    pass

class ShippingDetailsException(InvalidOrderOperation):
    pass

class VendorDetailsException(InvalidOrderOperation):
    pass

class ShippingOptionStrategyException(InvalidOrderOperation):
    pass

class OutOfStockException(InvalidOrderOperation):
    pass

class VendorNotFoundException(InvalidOrderOperation):
    pass

class VendorProductNotFoundException(InvalidOrderOperation):
    pass
