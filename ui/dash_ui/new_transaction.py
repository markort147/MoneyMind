import json
from datetime import date
from dash import html, dcc, callback, Output, Input, State, callback_context
import pandas as pd
from core import transactions


def display_page():
    categories = transactions.get_all_categories(as_dataframe=True)
    tags = transactions.get_all_tags(as_dataframe=True)
    tags = tags[tags['tag_name'] != '']

    return html.Div([
        html.Div(id='output-container'),
        dcc.Store(id='tags-store', data=tags.to_json(orient='split')),
        dcc.Store(id='transaction-to-be-inserted'),
        html.H1('MONEYMIND', style={'textAlign': 'center'}),
        html.H2('Are you more like Scrooge or Donald Duck?', style={'textAlign': 'center'}),
        html.Div([
            dcc.Link('Home', href='/', id='link-to-home-by-new-transaction'),
        ], style={'textAlign': 'center'}),
        html.Br(),
        html.Form([

            # description
            html.Div([
                html.Label('Description'),
                dcc.Input(type='text', id='input-description', placeholder='Enter description', value=''),
            ], style={'flex': '1'}),

            # amount
            html.Div([
                html.Label('Amount'),
                dcc.Input(type='text', id='input-amount', placeholder='Enter amount', value=''),
            ], style={'flex': '1'}),

            # recipient
            html.Div([
                html.Label('Recipient'),
                dcc.Input(type='text', id='input-recipient', placeholder='Enter recipient', value=''),
            ], style={'flex': '1'}),

            # date - pick date range - output format YYYY-MM-DD
            html.Div([
                html.Label('Date'),
                dcc.DatePickerSingle(
                    id='input-date',
                    initial_visible_month=date.today(),
                    date=date.today(),
                    display_format='MMM Do, YYYY',
                    clearable=False,
                    first_day_of_week=1
                ),
            ], style={'flex': '1'}),

            html.Datalist(
                id='suggested-categories',
                children=[html.Option(value=word) for word in categories['category_name'].tolist()]),

            # category
            html.Div([
                html.Label('Category'),
                dcc.Input(type='text', id='input-category', placeholder='Enter category', list='suggested-categories',
                          value=''),
            ], style={'flex': '1'}),

            # priority - dropdown among Voluntary, Needed and Mandatory - div size adapted to content
            html.Div([
                html.Label('Priority'),
                html.Div([
                    dcc.Dropdown(
                        id='input-priority',
                        options=[
                            {'label': 'Voluntary', 'value': 'Voluntary'},
                            {'label': 'Needed', 'value': 'Needed'},
                            {'label': 'Mandatory', 'value': 'Mandatory'},
                        ],
                        value='Voluntary',
                        clearable=False,
                    ),
                ])
            ], style={'flex': '1'}),

            # method
            html.Div([
                html.Label('Method'),
                dcc.Input(type='text', id='input-method', placeholder='Enter method', value=''),
            ], style={'flex': '1'}),

            # account
            html.Div([
                html.Label('Account'),
                dcc.Input(type='text', id='input-account', placeholder='Enter account', value=''),
            ], style={'flex': '1'}),

            # installment - boolean dropdown
            html.Div([
                html.Label('Installment'),
                dcc.Dropdown(
                    id='input-installment',
                    options=[
                        {'label': 'Yes', 'value': '1'},
                        {'label': 'No', 'value': '0'},
                    ],
                    value='0',
                    clearable=False,
                ),
            ], style={'flex': '1'}),

            # automatic - boolean dropdown
            html.Div([
                html.Label('Automatic'),
                dcc.Dropdown(
                    id='input-automatic',
                    options=[
                        {'label': 'Yes', 'value': '1'},
                        {'label': 'No', 'value': '0'},
                    ],
                    value='0',
                    clearable=False,
                ),
            ], style={'flex': '1'}),

            html.Datalist(
                id='suggested-tags',
                children=[html.Option(value=word + ';') for word in tags['tag_name'].tolist()]),

            # tags
            html.Div([
                html.Label('Tags'),
                html.Br(),
                dcc.Input(type='text', id='input-tags', placeholder='Enter tags', list='suggested-tags', value='')
            ], style={'flex': '1'}),

        ], style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '20px', 'justifyContent': 'center'}),

        # submit button
        html.Br(),
        html.Div([
            html.Button('Submit', id='submit-button-new-transaction', n_clicks=0)
        ], style={'text-align': 'center'}),

        # insert button
        html.Br(),
        html.Div(id='insert-div-button-new-transaction', style={'text-align': 'center'})
    ])


@callback(
    Output('suggested-tags', 'children'),
    Input('input-tags', 'value'),
    State('suggested-tags', 'children'),
    State('tags-store', 'data')
)
def update_suggested_tags(inserted_tags, current_suggested_tags, stored_tags):
    df = pd.read_json(stored_tags, orient='split')
    if inserted_tags is not None and len(inserted_tags) > 0 and ';' in inserted_tags:
        df = df[~df['tag_name'].isin(inserted_tags.split(';'))]
        if inserted_tags[-1] == ';':
            return [html.Option(value=inserted_tags + word) for word in df['tag_name'].tolist()]
        else:
            return [html.Option(value=inserted_tags + ';' + word) for word in df['tag_name'].tolist()]
    else:
        return [html.Option(value=word + ';') for word in df['tag_name'].tolist()]


@callback(
    Output('insert-div-button-new-transaction', 'children'),
    Output('transaction-to-be-inserted', 'data'),
    Input('submit-button-new-transaction', 'n_clicks'),
    State('input-description', 'value'),
    State('input-amount', 'value'),
    State('input-recipient', 'value'),
    State('input-date', 'date'),
    State('input-category', 'value'),
    State('input-priority', 'value'),
    State('input-method', 'value'),
    State('input-account', 'value'),
    State('input-installment', 'value'),
    State('input-automatic', 'value'),
    State('input-tags', 'value'),
)
def create_insert_button(n_clicks, description, amount, recipient, date_input, category, priority, method, account,
                         installment, automatic, tags):
    if n_clicks > 0:
        try:
            print('Validating')
            print('Date: {}'.format(date_input))
            description = transactions.validate_description(description)
            amount = transactions.validate_amount(amount)
            recipient = transactions.validate_recipient(recipient)
            date_input = transactions.validate_date(date_input)
            category = transactions.validate_category(category)
            priority = transactions.validate_priority(priority)
            method = transactions.validate_method(method)
            account = transactions.validate_account(account)
            installment = transactions.validate_installment(installment)
            automatic = transactions.validate_automatic(automatic)
            tags = transactions.validate_tags(tags)
            print('Validated')
            return html.Button('Insert', id='insert-button-new-transaction', n_clicks=0), json.dumps([description, amount, recipient, date_input, category, priority, method, account, installment, automatic, tags])
        except ValueError as e:
            # return a html red text bos with error
            print(e)
            return html.Div(str(e), style={'color': 'red'}), ''
    return [], ''


@callback(
    Output('output-container', 'children'),
    Input('insert-button-new-transaction', 'n_clicks'),
    State('transaction-to-be-inserted', 'data')
)
def insert_transaction(n_clicks, data):
    if n_clicks > 0:
        description, amount, recipient, date_input, category, priority, method, account, installment, automatic, tags = json.loads(data)
        transactions.insert_transaction(description=description, amount=amount, recipient=recipient, date_input=date_input, category=category, priority=priority, method=method, account=account, installment=installment, automatic=automatic, tags=tags)
    return
