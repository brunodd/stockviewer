from dataclasses import dataclass
from typing import Optional


@dataclass
class StockInfo:
    ticker: str
    full_name: str
    current_price: float

@dataclass
class StockOwnership:
    ticker: str
    buyPrice: float
    amount: Optional[int] = 0
