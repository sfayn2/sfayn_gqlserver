class DomainError(Exception):
    pass

class InvalidOrderOperation(DomainError):
    pass

class MoneyException(InvalidOrderOperation):
    pass

class AddressException(InvalidOrderOperation):
    pass

# below Exceptions will not be include error msg in response
class Forbidden(Exception):
    pass

class AccessControlException(Exception):
    pass

class IntegrationException(Exception):
    pass
