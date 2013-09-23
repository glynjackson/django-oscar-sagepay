import uuid
import datetime
from base64 import b32encode
from urllib import urlencode


def get_new_transaction_id():
    return _generate_transaction_id()


def _generate_transaction_id():
    """
    Generate a new transaction ID
    :return: unique value for each transaction.
    """
    return b32encode(uuid.uuid4().bytes).strip('=').lower()


def convert_date(date):
    """
    SagePay requires date fields to be 4 digits in MMYY (Month Year) format with no separators.
    """
    return datetime.datetime.strptime(str(date), '%Y-%m-%d').strftime('%m%y')


def get_card_type(number):
    """
    Gets credit card type given number. Based on values from Wikipedia page
    "Credit card number".
    http://en.wikipedia.org/w/index.php?title=Credit_card_number
    MC is MasterCard. UKE is Visa Electron. MAESTRO should be used for both UK and International Maestro.
    AMEX, DC (DINERS) and PAYPAL can only be accepted if you have additional merchant accounts with thos
    e acquirers.
    """
    number = str(number)
    #group checking by ascending length of number
    if len(number) == 13:
        if number[0] == "4":
            return "VISA"
    elif len(number) == 14:
        if number[:2] == "36":
            return "MC"
    elif len(number) == 15:
        if number[:2] in ("34", "37"):
            return "AMEX"
    elif len(number) == 16:
        if number[:4] == "6011":
            return "Discover"
        if number[:2] in ("51", "52", "53", "54", "55"):
            return "MC"
        if number[0] == "4":
            return "VISA"
    return "Unknown"


def encode_transaction_request(data):
    # We're going to mutate this dict so make a copy
    data = data.copy()
    for key in data:
        if not isinstance(data[key], basestring):
            data[key] = unicode(data[key])
        data[key] = data[key].encode('utf8')

    return urlencode(data)


def extract_address_data(address):
    data = {}
    if not address:
        return data
    for i in range(1, 5):
        key = 'line%d' % i
        if hasattr(address, key):
            data['address_line%d' % i] = getattr(address, key)
    data['postcode'] = address.postcode
    return data
