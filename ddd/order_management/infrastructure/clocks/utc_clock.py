import pytz
from datetime import datetime, time
from ddd.order_management.application import (
    ports
)

class UtcClock(ports.ClockAbstract):
    def now(self) -> time:
        return datetime.now(pytz.utc).time()