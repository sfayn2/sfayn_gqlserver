class InvalidOrderOperation(Exception):
    pass


class InvalidStatusTransitionError(Exception):
    pass

class InvalidOfferOperation(InvalidOrderOperation):
    pass


class InvalidPaymentOperation(InvalidOrderOperation):
    pass

class InvalidTaxOperation(InvalidOrderOperation):
    pass

class InvalidShippingOption(InvalidOrderOperation):
    pass

class InvalidVendorDetails(InvalidOrderOperation):
    pass

class OutOfStockException(InvalidOrderOperation):
    pass