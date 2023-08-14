from dash import Dash, html, dcc, callback, Output, Input, State
from config.config import Config
from ui.dash_ui import graphs_page, new_transaction
import dash_bootstrap_components as dbc


@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def change_page(pathname):
    if pathname == '/graphs':
        return graphs_page.display_page()
    if pathname == '/new-transaction':
        return new_transaction.display_page()
    else:
        return display_page()


def display_page():
    return html.Div([
        html.H1('MONEYMIND', style={'textAlign': 'center'}),
        html.H2('Don\'t you like the smell of nickel in the morning?', style={'textAlign': 'center'}),
        html.Br(),
        html.Div([
            dcc.Link('New transaction', href='/new-transaction', id='link-to-new-transaction'),
        ], style={'textAlign': 'center'}),
        html.Br(),
        html.Div([
            dcc.Link('Graphs', href='/graphs', id='link-to-graphs')
        ], style={'textAlign': 'center'})
    ])


def start():
    config = Config.get_instance()
    app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY], suppress_callback_exceptions=True)

    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(children=display_page(), id='page-content')
    ])

    app.run(debug=config.get_property('dash.debug'), port=config.get_property('dash.port'))
