from dash import Dash, html, dcc, callback, Output, Input, State
import pandas as pd
import plotly.express as px

from config.config import Config
from core import transactions


@callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/graphs':
        return graphs_page()
    else:
        return home_page()


def home_page():
    return html.Div([
        html.H1('MONEYMIND', style={'textAlign': 'center'}),
        html.H2('I like the smell of money in the morning', style={'textAlign': 'center'}),
        dcc.Link('View graphs', href='/graphs', id='link-to-graphs')
    ])


def graphs_page():
    return html.Div([
        html.H1('MONEYMIND', style={'textAlign': 'center'}),
        html.H2('I like the smell of money in the morning', style={'textAlign': 'center'}),
        dcc.Link('Back to home page', href='/', id='link-to-home'),
        # show a bar graph aggregating transactions by priority
        dcc.Graph(id='bar-graph-by-priority', figure=bar_graph_by_priority()),
    ])


def bar_graph_by_priority():
    df = transactions.get_all_transactions(as_dataframe=True)[['priority', 'amount']]
    df = df.groupby('priority').sum().reset_index()
    df['priority'] = pd.Categorical(df['priority'], categories=['mandatory', 'needed', 'voluntary'], ordered=True)
    df = df.sort_values(by=['priority'], ascending=False)
    normalized_values = df['amount'].apply(lambda x: '{:.1f}%'.format(100 * x / df['amount'].sum()))
    df['proportion'] = normalized_values
    fig = px.bar(df, y='priority', x='amount', color='priority',
                 color_discrete_map={'mandatory': 'red', 'needed': 'orange', 'voluntary': 'blue'}, text='proportion',
                 hover_name='priority', orientation='h')
    return fig


def start():
    config = Config.get_instance()
    app = Dash(__name__)

    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(children=home_page(), id='page-content')
    ])

    app.run(debug=config.get_property('dash.debug'), port=config.get_property('dash.port'))
