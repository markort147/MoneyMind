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
