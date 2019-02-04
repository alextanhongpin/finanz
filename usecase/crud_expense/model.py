from datetime import timezone, datetime
from dataclasses import dataclass, field


def now():
    datetime.now(timezone.utc).astimezone().isoformat()


@dataclass
class Expense:
    id: str
    name: str
    amount: int
    description: str = field(default='')
    created_at: str = field(default=now())


# How to serialize dataclasses back to json.
