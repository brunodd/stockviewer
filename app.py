from datetime import date, timedelta

import pandas as pd

from stockviewer.data.Activity import Activity, activities_to_df
from stockviewer.function.function import enrich, build_dataset, build_portfolio, portfolio_value

if __name__ == '__main__':
    # Parse activities
    activities = [
        Activity('2021-01-04', 'AAPL', 10, 130),
        Activity('2021-01-11', 'AAPL', -5, 150),
        Activity('2021-01-08', 'VGP.BR', 10, 150),
        Activity('2021-01-12', 'VGP.BR', 10, 150),

    ]

    activity_df = activities_to_df(activities)

    start_date = str(activity_df.index.min()).split()[0]
    end_date = date.today() - timedelta(days=1)

    ticker_symbols = activity_df.ticker.drop_duplicates()
    dataset = build_dataset(ticker_symbols, start_date, end_date)

    portfolio = build_portfolio(dataset, activity_df)
    print(portfolio_value(portfolio))


