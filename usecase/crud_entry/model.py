import datetime
from datetime import timezone
from dataclasses import dataclass, field


@dataclass
class Expense:
    id: str
    name: str
    amount: int
    description: str = field(default='')
    created_at: str = field(
        default=datetime.datetime.now(timezone.utc).astimezone().isoformat())
