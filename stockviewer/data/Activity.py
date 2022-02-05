from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class Activity:
    date: str
    ticker: str
    delta: int
    price: float


def activities_to_df(activities: List[Activity]) -> pd.DataFrame:
    df = pd.DataFrame(activities)
    df.index = pd.to_datetime(df.date)
    return df[['ticker', 'delta', 'price']].sort_index()