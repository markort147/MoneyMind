from dash import html, dcc, callback, Output, Input, State, callback_context, dash_table
import pandas as pd
import plotly.express as px
from core import transactions


def display_page():
    transactions_df = transactions.get_all_transactions(as_dataframe=True)

    return html.Div([
        dcc.Store(id='stored-original-show-transactions', data=transactions_df.to_json(orient='records')),

        html.H1('MONEYMIND', style={'textAlign': 'center'}),
        html.H2('Let\'s be tabular, my dear', style={'textAlign': 'center'}),
        html.Div([
            dcc.Link('Home', href='/', id='link-to-home-by-show-transactions'),
        ], style={'textAlign': 'center'}),
        html.Br(),
        html.Div(
            html.Button('Cancel edits', id='cancel-edits-button', n_clicks=0)
        ),
        html.Div(
            children=show_table(transactions_df),
            id='show-transactions-table'
        )
    ])


@callback(
    Output('show-transactions-table', 'children'),
    Input('cancel-edits-button', 'n_clicks'),
    State('stored-original-show-transactions', 'data')
)
def cancel_edits(n_clicks, stored_data):
    transactions_df = pd.read_json(stored_data, orient='records')
    return show_table(transactions_df)


def show_table(df):
    return dash_table.DataTable(df.to_dict('records'),
                                columns=[
                                    {
                                        "name": i,
                                        "id": i,
                                        "editable": True,
                                        "hideable": True,
                                        "filter_options": {'case': 'insensitive'}
                                    } for i in df.columns],
                                filter_action='native',
                                sort_action='native',
                                sort_mode='multi',
                                sort_by=[{'column_id': 'date', 'direction': 'asc'}],
                                style_data_conditional=(
                                    data_bars(df, 'amount')
                                ),
                                id='show-table')


def data_bars(df, column):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
        for i in bounds
    ]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        styles.append({
            'if': {
                'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'background': (
                """
                    linear-gradient(90deg,
                    #0074D9 0%,
                    #0074D9 {max_bound_percentage}%,
                    white {max_bound_percentage}%,
                    white 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'paddingBottom': 2,
            'paddingTop': 2
        })

    return styles
