from dash import html, dcc, callback, Output, Input, State
import pandas as pd
import plotly.express as px
from core import transactions


def display_page():
    categories = transactions.get_all_categories(as_dataframe=True)['category_name'].sort_values().unique()
    tags = transactions.get_all_tags(as_dataframe=True)['tag_name'].sort_values().unique()
    transactions_df = transactions.get_all_transactions(as_dataframe=True);

    return html.Div([
        dcc.Store(id='transactions-store'),
        dcc.Store(id='transactions-original',
                  data=transactions_df.to_json(orient='records', date_format='iso')),
        html.H1('MONEYMIND', style={'textAlign': 'center'}),
        html.H2('Let\'s view some graphs, my dear', style={'textAlign': 'center'}),
        html.Div([
            dcc.Link('Home', href='/', id='link-to-home')
        ], style={'textAlign': 'center'}),
        html.Div([
            html.Div([
                html.Label('Categories:'),
                dcc.Dropdown(options=categories, placeholder='Select categories',
                             id='categories-dropdown', multi=True)
            ], style={'padding': 10, 'flex': 1}),
            html.Div([
                html.Label('Tags:'),
                dcc.Dropdown(options=tags, placeholder='Select tags', id='tags-dropdown', multi=True)
            ], style={'padding': 10, 'flex': 1}),
            html.Div([
                html.Label('Date range:'),
                html.Br(),
                dcc.DatePickerRange(id='date-picker-range', display_format='DD/MM/YYYY',
                                    start_date=transactions_df['date'].min(), end_date=transactions_df['date'].max())
            ], style={'padding': 10, 'flex': 1})
        ], style={'display': 'flex', 'flex-direction': 'row', 'width': '50%', 'margin': 'auto'}),
        html.Div([
            html.Div([
                dcc.Graph(id='bar-graph-by-priority')
            ], style={'display': 'inline-block'}),
            html.Div([
                dcc.Graph(id='time-graph')
            ], style={'display': 'inline-block'})
        ], style={'textAlign': 'center'})
    ])


@callback(
    Output('transactions-store', 'data'),
    Input('categories-dropdown', 'value'),
    Input('tags-dropdown', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    State('transactions-original', 'data')
)
def update_transactions(categories, tags, start_date, end_date, jsonized_transactions_original):
    df = pd.read_json(jsonized_transactions_original, orient='records')

    if categories is not None and len(categories) > 0:
        df = df[df['category'].isin(categories)]

    if tags is not None and len(tags) > 0:
        s = set(tags)
        df = df[df['tags'].apply(lambda x: len(s.intersection(set(x.split(';')))) > 0)]

    df = df[df['date'].between(start_date, end_date)]

    return df.to_json(orient='records', date_format='iso')


@callback(
    Output('bar-graph-by-priority', 'figure'),
    Input('transactions-store', 'data')
)
def priority_bar_graph(jsonized_transactions):
    df = pd.read_json(jsonized_transactions, orient='records')
    df = df[['priority', 'amount']]
    df = df.groupby('priority').sum().reset_index()

    priority_order = ['mandatory', 'needed', 'voluntary']
    for value in priority_order.copy():
        if value not in df['priority'].unique():
            priority_order.remove(value)

    df['priority'] = pd.Categorical(df['priority'], categories=priority_order, ordered=True)
    df = df.sort_values(by=['priority'], ascending=False)

    normalized_values = df['amount'].apply(lambda x: '{:.1f}%'.format(100 * x / df['amount'].sum()))
    df['proportion'] = normalized_values

    color_map = {'mandatory': 'red', 'needed': 'orange', 'voluntary': 'blue'}
    for key, value in color_map.copy().items():
        if key not in df['priority'].unique():
            color_map.pop(key)

    fig = px.bar(df, y='priority', x='amount', color='priority',
                 color_discrete_map=color_map, text='proportion',
                 hover_name='priority', orientation='h', title='Priority by amount')

    return fig


@callback(
    Output('time-graph', 'figure'),
    Input('transactions-store', 'data')
)
def time_graph(jsonized_transactions):
    df = pd.read_json(jsonized_transactions, orient='records')
    df = df[['date', 'amount']]
    df = df.groupby('date').sum().reset_index()

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'], ascending=False)

    fig = px.bar(df, x='date', y='amount', title='Amounts by time')

    return fig
