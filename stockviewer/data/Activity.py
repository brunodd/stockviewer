import os
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
    df.index = pd.to_datetime(df.date, infer_datetime_format=True)
    return df[['ticker', 'delta', 'price']].sort_index()


def read_activities() -> pd.DataFrame:
    df = pd.read_csv(os.path.join(
        os.getenv("DATA_VOLUME", '/Users/brunodedeken/Projects/Personal/stockviewer/data'),
        'activity.csv')
    )
    df.index = pd.to_datetime(df.date, infer_datetime_format=True)
    result = df[['ticker', 'delta', 'price']].sort_index()
    return result

