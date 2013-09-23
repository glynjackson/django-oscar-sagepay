import re
import httplib
import urllib
import urllib2
import webbrowser
import logging



from oscar.apps.payment.exceptions import GatewayError

from .utils import get_new_transaction_id, get_card_type, convert_date, \
    encode_transaction_request, extract_address_data


logger = logging.getLogger('sagepay')


class Gateway(object):
    def __init__(self, vendor, password, currency, transaction_mode):
        self._vendor = vendor
        self._password = password
        self._currency = currency
        self._transaction_mode = transaction_mode
        self._basket_field_length = 7500
        self._field_lengths = (
            ('Description', 100),
            ('CustomerEMail', 255),
        )
        self._invalid_chars = re.compile("( [\x00-\x1f\x7f-\xff] | : )", re.UNICODE | re.VERBOSE)

        # ===========
        # API Calls
        # ===========

    def auth(self, **kwargs):
        """
        Performs an 'auth' request, which is to debit the money immediately
        as a one-off transaction.
        """
        return self._do_request(TxType='PAYMENT', **kwargs)


    def refund(self, **kwargs):
        """
        Refund against a card
        """
        return self._do_request(TxType='REFUND', **kwargs)


        # ===============
        # END API Calls
        # ===============

    def _do_request(self, TxType, **kwargs):
        """
         Actually make a request to the gateway.
        :param TxType: Type of request you will be making, i.e. Payment, Pre-Auth, Refund.
        :param kwargs:
        :return: dict: Response from gateway.
        """

        data = {
            'TxType': TxType,
            }
        # Add all shipping/delivery data to the post.
        data.update(self._build_shipping_address(extract_address_data(kwargs['shipping_address'])))
        # Add billing information.

        # Add all other final post settings.
        data.update(self._build_post(**kwargs))

        print("=============")

        print(data)

        print("=============")

        request_body = encode_transaction_request(data)
        # Get API URLs there will be based on the transaction mode in settings.
        url = self.get_gateway_urls()['AUTHORISE']
        # Fire request to SagePay.
        results = urllib2.urlopen(url, request_body)
        # Create the response object.
        response = Response(response=results.read(), data=data)

        # Do some logging.
        if response.is_successful():
            logger.info("Successful response, SagePay ref: %s",
            response.get_VPSTxId())
            print("OK=================")
        else:
            logger.warning("Unsuccessful response, SagePay ref: %s",
                            response.get_VendorTxCode())
            print("BAD=================")
        # Return the response object.
        return response




    def _build_shipping_address(self, address):
        data = {}
        if not address:
            return data
        data ={
            'DeliverySurname': 'SASa',
            'DeliveryFirstnames': 'ssaas',
            'DeliveryAddress1': address['address_line1'],
            'DeliveryCity': 'sasa',
            'DeliveryPostCode': address['postcode'],
            'DeliveryCountry': 'GB',
        }
        return data

    def _build_billing_address(self, address):
        """
        Builds the billing address
        :param address: as dict
        :return: data dict: billing address
        """
        data = {}
        if not address:
            return data
        data ={
            'BillingSurname': 'SASa',
            'BillingFirstnames': 'ssaas',
            'BillingAddress1': 'sasasa',
            'BillingCity': 'sasa',
            'BillingPostCode': 'ST71GB',
            'BillingCountry': 'GB',
        }
        return data


    def _build_post(self, **kwargs):
        """
        Builds the POST for a transaction
        :param kwargs:
        :return: data
        """

        data = {
            'VPSProtocol': '2.23',
            'VendorTxCode': get_new_transaction_id(),
            'Vendor': self._vendor,
            'Currency': self._currency,
            'Amount': str(kwargs['amount']),
            'CardHolder': 'AAAAAAAA',
            'CardNumber': kwargs['card_number'],
            'ExpiryDate': convert_date(kwargs['expiry_date']),
            'CV2': kwargs['ccv'],
            'CardType': get_card_type(kwargs['card_number']),
            'CreateToken': 1,




            }
        return data

    def _build_gateway_urls(self):
        """
        Gives us all the API URLs needed to contact SagePay. URLs are based on the transaction mode in settings.
        :return: dict of API URLs.
        """
        if self._transaction_mode == 'Simulator':
            urls = {
                'MODE': 'Simulator',
                'AUTHORISE': 'https://test.sagepay.com/Simulator/VSPDirectGateway.asp?Service=VendorAuthoriseTx',
                }
        elif self._transaction_mode == 'Test':
            urls = {
                'MODE': 'Test',
                'AUTHORISE': 'https://test.sagepay.com/gateway/service/vspserver-register.vsp',
                }

        elif self._transaction_mode == 'Live':
            urls = {
                'MODE': 'Live',
                'AUTHORISE': 'https://live.sagepay.com/gateway/service/vspserver-register.vsp',
                }
        else:
            raise RuntimeError("No Transaction mode for SagePay")
        return urls

    def get_gateway_urls(self):
        """
        Get method  that gives us all the API URLs needed to contact SagePay.
        :return: a list of API URLs based on the transaction mode.
        """
        return self._build_gateway_urls()


class Response(object):
    """
    Encapsulate a SagePay response
    Response object needs the response string itself and the data (dict) that was originally sent to the gateway.
    """

    def __init__(self, response, data):
        self.raw_response = response
        self.response = self._decode_transaction_response(response)
        self.data = data
        print("==================")
        print(self.response)
        print("==================")

    def _decode_transaction_response(self, body):
        return dict(line.split('=', 1) for line in body.strip().split("\r\n"))

    def get_raw_response(self):
        return self.raw_response

    def get_status(self):
        """
        Gets and returns the status of the response.
        :return: returns status i.e. OK, MALFORMED etc.
        """
        return self.response['Status']

    def get_status_message(self):
        """
        Gets and returns the message status of the response.
        If the status is not OK, the StatusDetail field will give
        more information about the status.
        :return:
        """
        if self.is_successful():
            return "Status was OK, no details"
        else:
            return self.response['StatusDetail']

    def is_successful(self):
        """
        Confirms if a response was successful.
        :return: boolean True if status OK is found in the response.
        """
        if self.get_status() == 'OK':
            return True
        else:
            return False

    def is_declined(self):
        if self.get_status() == 'NOTAUTHED':
            return True
        else:
            return False

    def is_rejected(self):
        if self.get_status() == 'REJECTED':
            return True
        else:
            return False


    def get_sagepay_ref(self):
        """
        :return:
        """
        pass

    def get_VPSTxId(self):
        """
        VPSTxId, is a unique transaction reference only given if auth was OK.
        :return:
        """
        return self.response['VPSTxId']

    def get_SecurityKey(self):
        return self.response['SecurityKey']

    def get_VendorTxCode(self):
        return self.data['VendorTxCode']







