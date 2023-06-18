from ....ordering_domain import abstract_domain_models

class Ordering(abstract_domain_models.AggregateRoot):

    def __init__(self):
        pass

    def set_entity_id(self, entity_id: str):
        self._entity_id = entity_id

    def set_buyer_note(self, buyer_note: str):
        if buyer_note:
            self._buyer_note = buyer_note
        else:
            self._buyer_note = None