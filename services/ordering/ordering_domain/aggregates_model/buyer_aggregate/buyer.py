from ....ordering_domain import abstract_domain_models

class Buyer(abstract_domain_models.AggregateRoot):

    def __init__(self, 
                 buyer_id: str, 
                 buyer_note: str
                 ):
        
        self._buyer_id = buyer_id
        self._buyer_note = buyer_note


    def set_buyer_note(self, buyer_note: str):
        if not buyer_note:
            raise "Invalid empty buyer note!"
        self._buyer_note = buyer_note