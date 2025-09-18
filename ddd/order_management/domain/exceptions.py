class InvalidOrderOperation(Exception):
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

class WorkflowException(InvalidOrderOperation):
    pass