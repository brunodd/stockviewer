import plotly.express as px
from dash import dcc, html

from stockviewer.function.function import portfolio_value, compute_distribution


def build_dash_layout(app, portfolio):
    portfolio_evolution = portfolio_value(portfolio)
    portfolio_evolution_fig = px.line(portfolio_evolution.reset_index(), x='Date', y="total_value")

    latest_date = portfolio.index.max()
    portfolio_distribution = compute_distribution(portfolio, latest_date)
    portfolio_distribution_fig = px.pie(portfolio_distribution.reset_index(), values='perc', names='ticker',
                                        title='Portfolio distribution per ticker')

    app.layout = html.Div([
        html.H1(children="Stock Viewer", className="title",
                style={'color': '#00361c', 'text-align': 'center'
                       }),
        html.Div([
            dcc.Graph(id='portfolio-evolution', figure=portfolio_evolution_fig)
        ]),
        html.Div([
            dcc.Graph(id='portfolio-distribution', figure=portfolio_distribution_fig)
        ])
    ])
