# A transaction has the following fields:
# - amount
# - description
# - recipient
# - date
# - installment
# - category
# - priority
# - automatic
# - method
# - account
# - tags


import re
import datetime

from config.config import Config
from database.sqlite_repository import Database
import pandas as pd

REGEX_AMOUNT = r'^[\d]*((\.\d{0,3})|(\d))'
FORMAT_DATE = '%Y-%m-%d'
ENUM_INSTALLMENT = ['0', '1', '']
ENUM_PRIORITY = ['voluntary', 'needed', 'mandatory', 'v', 'n', 'm', '']
ENUM_AUTOMATIC = ['0', '1', '']
REGEX_TAGS = r'^(|[\w]+|[\w]+(;[\w]+)*)$'
DEFAULT_PRIORITY = 'voluntary'
DEFAULT_AUTOMATIC = '0'
DEFAULT_INSTALLMENT = '0'
MAP_PRIORITY = {
    '': DEFAULT_PRIORITY,
    'n': 'needed',
    'v': 'voluntary',
    'm': 'mandatory',
    'needed': 'needed',
    'voluntary': 'voluntary',
    'mandatory': 'mandatory'
}


def _validate_regex(regex_pattern, value):
    if re.match(regex_pattern, value) is not None:
        return True
    else:
        return False


def _validate_enum(enum_list, value):
    if value in enum_list:
        return True
    else:
        return False


def validate_amount(amount):
    if _validate_regex(REGEX_AMOUNT, amount):
        return float(amount)
    else:
        raise ValueError('Amount must be a number with at most three decimal places')


def validate_description(description):
    # description must be at most 255 characters long
    if len(description) <= 255:
        return description
    else:
        raise ValueError('Description must be at most 255 characters long')


def validate_recipient(recipient):
    # recipient must be at most 255 characters long not empty string
    if 0 < len(recipient) <= 255:
        return recipient
    else:
        raise ValueError('Recipient must be at most 255 characters long not empty string')


def validate_date(date_input):
    # date must be a string in the format YYYY-MM-DD or empty string
    if len(date_input) == 0:
        return datetime.date.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.datetime.strptime(date_input, FORMAT_DATE).date()
            return date_input
        except ValueError:
            raise ValueError('Date must be a string in the format YYYY-MM-DD or empty string')


def validate_installment(installment):
    if _validate_enum(ENUM_INSTALLMENT, installment):
        if len(installment) == 0:
            return DEFAULT_INSTALLMENT
        else:
            return installment
    else:
        raise ValueError('Installment must be 0, 1 or empty string')


def validate_category(category):
    # category must be at most 255 characters long not empty string
    if 0 < len(category) <= 255:
        return category
    else:
        raise ValueError('Category must be at most 255 characters long not empty string')


def validate_priority(priority):
    if _validate_enum(ENUM_PRIORITY, priority.lower()):
        return MAP_PRIORITY.get(priority.lower())
    else:
        raise ValueError('Priority must be voluntary, needed, mandatory, v, n, m or empty string')


def validate_automatic(automatic):
    if _validate_enum(ENUM_AUTOMATIC, automatic):
        if len(automatic) == 0:
            return DEFAULT_AUTOMATIC
        else:
            return automatic
    else:
        raise ValueError('Automatic must be 0, 1 or empty string')


def validate_method(method):
    # method must be at most 255 characters long not empty string
    if 0 < len(method) <= 255:
        return method
    else:
        raise ValueError('Method must be at most 255 characters long not empty string')


def validate_account(account):
    # account must be at most 255 characters long not empty string
    if 0 < len(account) <= 255:
        return account
    else:
        raise ValueError('Account must be at most 255 characters long not empty string')


def validate_tags(tags):
    # tags must be a word, a semicolon-separated list of words, or an empty string
    if _validate_regex(REGEX_TAGS, tags):
        return tags
    else:
        raise ValueError('Tags must be a word, a semicolon-separated list of words, or an empty string')


def insert_transaction(amount, description, recipient, date_input, installment, category, priority, automatic,
                       method, account, tags):
    # insert recipient
    recipient_id = Database.get_instance().execute_select(table='recipients', where={'recipient_name': recipient},
                                                          columns=('id',))
    if recipient_id is not None:
        recipient_id = recipient_id[0]
    else:
        recipient_id = Database.get_instance().execute_insert(table='recipients', values=(recipient,),
                                                              columns=('recipient_name',))

    # insert category
    category_id = Database.get_instance().execute_select(table='categories', where={'category_name': category},
                                                         columns=('id',))
    if category_id is not None:
        category_id = category_id[0]
    else:
        category_id = Database.get_instance().execute_insert(table='categories', values=(category,),
                                                             columns=('category_name',))

    # insert method
    method_id = Database.get_instance().execute_select(table='methods', where={'method_name': category},
                                                       columns=('id',))
    if method_id is not None:
        method_id = method_id[0]
    else:
        method_id = Database.get_instance().execute_insert(table='methods', values=(method,), columns=('method_name',))

    # insert account
    account_id = Database.get_instance().execute_select(table='accounts', where={'account_name': account},
                                                        columns=('id',))
    if account_id is not None:
        account_id = account_id[0]
    else:
        account_id = Database.get_instance().execute_insert(table='accounts', values=(account,),
                                                            columns=('account_name',))

    # insert tags
    tag_id_list = []
    tags_list = tags.split(';')
    for tag in tags_list:
        tag_id = Database.get_instance().execute_select(table='tags', where={'tag_name': tag}, columns=('id',))
        if tag_id is not None:
            tag_id = tag_id[0]
        else:
            tag_id = Database.get_instance().execute_insert(table='tags', values=(tag,), columns=('tag_name',))
        tag_id_list.append(str(tag_id))

    # insert transaction
    transaction_id = Database.get_instance().execute_insert(table='transactions',
                                                            values=(
                                                                amount, description, recipient_id, date_input,
                                                                installment, category_id, priority, automatic,
                                                                method_id, account_id, tags),
                                                            columns=('amount', 'description', 'recipient', 'date',
                                                                     'installment', 'category', 'priority',
                                                                     'automatic', 'method', 'account',
                                                                     'tags'))

    # insert transaction tags
    for tag_id in tag_id_list:
        Database.get_instance().execute_insert(table='transaction_tags', values=(transaction_id, tag_id))


def get_all_transactions(as_dataframe=False):
    transactions = Database.get_instance().execute_select(table='transactions_view', get_first=False)

    if as_dataframe:
        return pd.DataFrame(data=transactions,
                            columns=["id", "amount", "description", "recipient", "date", "installment", "category",
                                     "priority", "automatic", "method", "account", "tags"])
    else:
        return transactions


def delete_transaction(id_to_delete):
    Database.get_instance().execute_delete(table='transaction_tags', where={'id_transaction': id_to_delete})
    Database.get_instance().execute_delete(table='transactions', where={'id': id_to_delete})


def get_all_tags(as_dataframe=False):
    tags = Database.get_instance().execute_select(table='tags', get_first=False)

    if as_dataframe:
        return pd.DataFrame(data=tags, columns=["id", "tag_name"])
    else:
        return tags


def get_all_categories(as_dataframe=False):
    categories = Database.get_instance().execute_select(table='categories', get_first=False)

    if as_dataframe:
        return pd.DataFrame(data=categories, columns=["id", "category_name"])
    else:
        return categories


def import_from_file(format_file):
    import_properties = Config.get_instance().get_property('import')
    if format_file == 'csv':
        csv_file = import_properties['csv_file']
        df = pd.read_csv(csv_file, dtype=str)
        df.fillna('', inplace=True)
        # print(df.to_string())
        for index, row in df.iterrows():
            try:
                amount = validate_amount(row['amount'])
                description = validate_description(row['description'])
                recipient = validate_recipient(row['recipient'])
                date_input = validate_date(row['date'])
                installment = validate_installment(row['installment'])
                category = validate_category(row['category'])
                priority = validate_priority(row['priority'])
                automatic = validate_automatic(row['automatic'])
                method = validate_method(row['method'])
                account = validate_account(row['account'])
                tags = validate_tags(row['tags'])
                insert_transaction(amount, description, recipient, date_input, installment, category, priority,
                                   automatic, method, account, tags)
            except ValueError as e:
                raise ValueError('Error while inserting transaction {}: {}.'.format(index, str(e)))
