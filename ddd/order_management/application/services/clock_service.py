from __future__ import annotations
from datetime import time

class ClockService:

    #TODO for now MVP; do like this ; easy to evolve
    def __init__(self, clock_options):
        self.clock_option = clock_options

    def now(self) -> time:
        return self.clock_option[0].now()