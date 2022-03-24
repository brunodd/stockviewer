import datetime

import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output, State

from stockviewer.function.function import portfolio_value, compute_distribution, get_data_single_symbol


def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + datetime.timedelta(days=i) for i in range(delta.days + 1)]
    return days


def build_portfolio_layout(app, portfolio):
    portfolio_evolution = portfolio_value(portfolio)
    # min_date = portfolio.index.min()
    min_date = datetime.datetime.fromisoformat('2018-03-19')
    max_date = portfolio.index.max() - datetime.timedelta(days=1)

    print("min_date = {}".format(min_date))
    print("max_date = {}".format(max_date))
    portfolio_evolution_fig = px.line(portfolio_evolution.reset_index(), x='Date', y="total_value")
    portfolio_distribution = compute_distribution(portfolio, max_date)
    portfolio_distribution_fig = px.pie(portfolio_distribution.reset_index(), values='perc', names='ticker',
                                        title='Portfolio distribution per ticker')

    date_picker_div = dcc.DatePickerRange(
        id='datepickerrange',
        start_date=min_date.date(),
        end_date=max_date.date(),
        min_date_allowed=datetime.date.fromisoformat('2015-01-01'),
        max_date_allowed=datetime.date.today(),
        display_format='D-MM-YYYY'
    )

    title_div = html.Div([html.H1(children="Stock Viewer", className="title",
                                  style={'color': '#00361c', 'text-align': 'center'
                                         })])
    portfolio_evolution_div = html.Div([
        html.Div([
            dcc.Graph(id='portfolio-evolution', figure=portfolio_evolution_fig),
            dcc.Graph(id='portfolio-distribution', figure=portfolio_distribution_fig),
        ]),
    ])

    dynamic_ticker_details = html.Div([
        html.Div([
            dcc.Input(
                id="input-ticker",
                type='text',
                value='AAPL'
            ),
            html.Button('Submit', id='input-on-submit', n_clicks=0),
        ]),
        html.Div([
            html.Div([
                html.H2(children=f"Price", className="title",
                        style={'color': 'blue', 'text-align': 'center'}),
                dcc.Graph(id='ticker-detail-price'),
            ]),
            html.Div([
                html.H2(children=f"Dividends", className="title",
                        style={'color': 'blue', 'text-align': 'center'}),
                dcc.Graph(id='ticker-detail-dividend')
            ]),
        ]),

    ])

    app.layout = html.Div([
        title_div,
        date_picker_div,
        portfolio_evolution_div,
        dynamic_ticker_details
    ])

    @app.callback(
        Output('ticker-detail-price', 'figure'),
        State('input-ticker', 'value'),
        Input('input-on-submit', 'n_clicks'),
        Input('datepickerrange', 'start_date'),
        Input('datepickerrange', 'end_date'),

    )
    def ticker_price_render(input_ticker, _, start_date, end_date):
        if input_ticker:
            ticker_df = get_data_single_symbol(input_ticker, start_date, end_date).rename(
                columns={'Close': 'price_evolution'}).reset_index()
        else:
            ticker_df = pd.DataFrame({'Date': [], 'price_evolution': []})
        ticker_fig = px.line(ticker_df, x='Date', y='price_evolution')
        return ticker_fig

    @app.callback(
        Output('ticker-detail-dividend', 'figure'),
        State('input-ticker', 'value'),
        Input('input-on-submit', 'n_clicks'),
        Input('datepickerrange', 'start_date'),
        Input('datepickerrange', 'end_date'),

    )
    def ticker_price_render(input_ticker, _, start_date, end_date):
        if input_ticker:
            ticker_df = get_data_single_symbol(input_ticker, start_date, end_date).rename(
                columns={'Dividends': 'dividend'}).resample('Q').sum().reset_index()
        else:
            ticker_df = pd.DataFrame({'Date': [], 'dividend': []})
        ticker_fig = px.bar(ticker_df, x='Date', y='dividend')
        return ticker_fig

    app.css.append_css({
        'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
    })

    return app
