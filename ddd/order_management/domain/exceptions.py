
class ShippingProviderIntegrationError(Exception):
    pass

class InvalidOrderOperation(Exception):
    pass

class DomainError(InvalidOrderOperation):
    pass

class MoneyException(InvalidOrderOperation):
    pass

class AddressException(InvalidOrderOperation):
    pass

class AccessControlException(InvalidOrderOperation):
    pass


# below Exceptions will not be include error msg in response
class Forbidden(Exception):
    pass

class IntegrationException(Exception):
    pass
