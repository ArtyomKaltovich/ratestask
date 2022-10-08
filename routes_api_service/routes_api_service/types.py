from typing import TypedDict, Optional


class Rate(TypedDict):
    day: str
    average_price: Optional[float]
