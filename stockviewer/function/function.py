import numpy as np
import pandas as pd
import yfinance
from pandas import Timestamp

HISTORICAL_FIELDS = ['Close', 'Dividends']
BALANCE_FIELDS = ['Total Liab', 'Total Assets']


def get_ticker(symbol):
    return yfinance.Ticker(symbol)


def filter_available_fields(fields, available) -> list[str]:
    result = list()
    for f in fields:
        if f in available:
            result.append(f)
    return result

def get_balance_type(fields):
    assets = list()
    debts = list()
    for f in fields:
        if 'liab' in f.lower():
            debts.append(f)
        elif 'asset' in f.lower():
            assets.append(f)
    return (assets, debts)


def get_ticker_balance(symbol, freq='yearly') -> pd.DataFrame:
    """
    :param freq: 'yearly' or 'quarterly'
    """
    df = get_ticker(symbol).get_balancesheet(freq=freq)
    available = [str(i) for i in df.index.tolist()]
    print(df)
    print(available)
    fields = filter_available_fields(BALANCE_FIELDS, available)
    df = df.T[fields]
    asset_cols, debt_cols = get_balance_type(fields)
    print(asset_cols)
    print(df)
    df['assets'] = df.loc[:, asset_cols].sum(axis=1)
    df['debt'] = df.loc[:, debt_cols].sum(axis=1)
    # df['debt'] = df['Short Long Term Debt'] + df['Long Term Debt']
    # df['assets'] = df['Total Assets']
    df.index = pd.to_datetime(df.index)
    return df[['debt', 'assets']]


def get_ticker_historical(symbol, start_date, end_date) -> pd.DataFrame:
    return get_ticker(symbol) \
        .history(start=start_date, end=end_date)[HISTORICAL_FIELDS] \
        .reset_index().set_index('Date') \
        .resample('D', convention='end').asfreq() \
        .ffill().bfill()


def build_dataset(ticker_symbols, start_date, end_date) -> dict[str, pd.DataFrame]:
    dataset = dict()
    for ticker in ticker_symbols:
        df = get_ticker_historical(ticker, start_date, end_date)

        dataset[ticker] = df.rename(columns={'Close': ticker})
    return dataset


def enrich(ticker, dataset, activity_df):
    df1 = dataset[ticker]
    df1 = pd.merge(activity_df.loc[activity_df.ticker == ticker, ['delta', 'price']], df1, left_index=True,
                   right_index=True, how='right').rename(columns={'price': 'cost', ticker: 'price'})
    acc_fn = AccumulateActivity()
    df1['amount'] = df1['delta'].apply(acc_fn)
    df1['value'] = df1['price'] * df1['amount']
    df1['ticker'] = ticker
    return df1


def build_portfolio(dataset, activity_df):
    return pd.pivot(
        pd.concat([enrich(x, dataset, activity_df) for x in dataset.keys()]).sort_index(),
        columns=['ticker']
    ).swaplevel(axis=1)


def portfolio_value(portfolio: pd.DataFrame) -> pd.DataFrame:
    # Retrieve stock count per day
    values = portfolio.iloc[:, portfolio.columns.get_level_values(1) == 'value'].sum(axis=1).reset_index()
    values.index = pd.to_datetime(values.Date)
    values = values.loc[:, [0]].rename(columns={0: 'total_value'})
    return values


def compute_distribution(portfolio: pd.DataFrame, date: Timestamp) -> pd.DataFrame:
    distribution = (
        portfolio
            .loc[
            [date],
            portfolio.columns.get_level_values(1) == 'value']
            .transpose()
            .reset_index().set_index('ticker')[[date]]
            .rename(columns={date: 'value'})
    )

    distribution['perc'] = distribution['value'] / distribution['value'].sum()
    return distribution


class AccumulateActivity:
    def __init__(self):
        self.state = 0

    def __call__(self, v):
        value = v
        if (np.isnan(value)):
            return self.state
        else:
            result = self.state + value
            self.state = result
        return result
