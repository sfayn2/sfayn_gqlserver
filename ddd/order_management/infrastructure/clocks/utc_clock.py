from datetime import datetime, timezone
from ddd.order_management.domain import (
    services
)

class UTCClock(services.ClockAbstract):
    def now(self) -> datetime:
        return datetime.now(tz=timezone.utc)