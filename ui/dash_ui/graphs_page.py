from dash import html, dcc, callback, Output, Input, State, callback_context
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
        html.H2('Let\'s be graphical, my dear', style={'textAlign': 'center'}),
        html.Div([
            dcc.Link('Home', href='/', id='link-to-home')
        ], style={'textAlign': 'center'}),
        html.Br(),
        html.Div([
            html.Div([
                html.Label('Categories:'),
                dcc.Dropdown(options=categories, placeholder='Select categories',
                             id='categories-dropdown', multi=True)
            ], style={'padding': 10, 'flex': 2}),
            html.Div([
                html.Label('Tags:'),
                dcc.Dropdown(options=tags, placeholder='Select tags', id='tags-dropdown', multi=True)
            ], style={'padding': 10, 'flex': 2}),
            html.Div([
                html.Label('Date range:'),
                html.Br(),
                dcc.DatePickerRange(id='date-picker-range', display_format='DD/MM/YYYY',
                                    start_date=transactions_df['date'].min(), end_date=transactions_df['date'].max())
            ], style={'padding': 10, 'flex': 5}),
            html.Div([
                html.Br(),
                html.Button('Submit', id='submit-button', n_clicks=0),
                html.Br(),
                html.Button('Reset', id='reset-button', n_clicks=0),
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
    Output('categories-dropdown', 'value'),
    Output('tags-dropdown', 'value'),
    Output('date-picker-range', 'start_date'),
    Output('date-picker-range', 'end_date'),
    Output('transactions-store', 'data'),
    Input('reset-button', 'n_clicks'),
    Input('submit-button', 'n_clicks'),
    State('categories-dropdown', 'value'),
    State('tags-dropdown', 'value'),
    State('date-picker-range', 'start_date'),
    State('date-picker-range', 'end_date'),
    State('transactions-original', 'data')
)
def update_transactions(n_clicks_reset_button, n_clicks_submit_button, categories, tags, start_date, end_date,
                        jsonized_transactions_original):
    callback_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    df = pd.read_json(jsonized_transactions_original, orient='records')

    if callback_id == 'submit-button':

        if categories is not None and len(categories) > 0:
            df = df[df['category'].isin(categories)]

        if tags is not None and len(tags) > 0:
            s = set(tags)
            df = df[df['tags'].apply(lambda x: len(s.intersection(set(x.split(';')))) > 0)]

        df = df[df['date'].between(start_date, end_date)]
        categories = df['category'].unique().tolist()
        tag_lists = df['tags'].apply(lambda x: x.split(';')).tolist()
        tag_set = set()
        for tag_list in tag_lists:
            tag_set.update(tag_list)
        tags = list(tag_set)

        start_date = df['date'].min()
        end_date = df['date'].max()

        return categories, tags, start_date, end_date, df.to_json(orient='records', date_format='iso')

    else:
        return [], [], df['date'].min(), df['date'].max(), jsonized_transactions_original


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
