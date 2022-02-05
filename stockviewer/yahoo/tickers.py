import yfinance as yf

from stockviewer.data.StockInfo import StockInfo


def fetch_ticker(ticker: str) -> StockInfo:
    obj = yf.Ticker(ticker)
    info = parse(obj)
    return info


def parse(obj: yf.Ticker) -> StockInfo:
    return StockInfo(
        ticker=obj.info.get('symbol'),
        full_name=obj.info.get('longName'),
        current_price=obj.info.get('currentPrice')
    )
