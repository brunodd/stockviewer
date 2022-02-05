from datetime import date, timedelta

from stockviewer.data.Activity import Activity, activities_to_df
from stockviewer.function.function import build_dataset, build_portfolio, portfolio_value
import plotly.express as px

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
    df = portfolio_value(portfolio)

    fig = px.line(df.reset_index(), x='Date', y="total_value")
    fig.show()
