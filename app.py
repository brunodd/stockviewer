from datetime import timedelta, date

import dash

from stockviewer.data.Activity import read_activities
from stockviewer.function.function import build_dataset, build_portfolio
from stockviewer.gui.dash import build_portfolio_layout
# from stockviewer.gui.example_dash import build_portfolio_layout

activity_df = read_activities()

start_date = str(activity_df.index.min()).split()[0]
end_date = date.today() - timedelta(days=1)

ticker_symbols = activity_df.ticker.drop_duplicates()
dataset = build_dataset(ticker_symbols, start_date, end_date)

portfolio = build_portfolio(dataset, activity_df)

app = dash.Dash()
server = app.server
app = build_portfolio_layout(app, portfolio)
# app = build_detail_layout(app, 'AAPL')

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8080)
