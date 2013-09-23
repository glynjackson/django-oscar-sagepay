from django.conf import settings

from oscar.apps.payment.exceptions import UnableToTakePayment, InvalidGatewayRequestError

from .gateway import Gateway
from .models import SagePayTransaction


class Facade(object):
    """
    In the style of django-oscar-datacash - A bridge between oscar's objects and the core gateway object, nice idea!
    """

    def __init__(self):
        self.gateway = Gateway(
            settings.SAGEPAY_VENDOR,
            settings.SAGEPAY_PASSWORD,
            settings.SAGEPAY_CURRENCY,
            settings.SAGEPAY_MODE,
            )

    def get_transaction_urls(self):
        return self.gateway.get_gateway_urls()



    def authorise(self, order_number, amount, bankcard=None,
                  txn_reference=None, billing_address=None, shipping_address=None):
        """

        :param order_number:
        :param amount:
        :param bankcard:
        :param txn_reference:
        :param billing_address: string: full shipping address
        :param shipping_address: string: full shipping address
        :return:
        """


        if amount == 0:
            raise UnableToTakePayment("Order amount must be non-zero")

        print("skasakskakskakskakjksjkjsakjakjkjkjkajkjaskajskjsaksajkjaskjsakjsakjsjsakjasjakzjakjaskjasj====")
        print(billing_address)
        print("skasakskakskakskakjksjkjsakjakjkjkjkajkjaskajskjsaksajkjaskjsakjsakjsjsakjasjakzjakjaskjasj====")
        response = self.gateway.auth(
            card_number=bankcard.card_number,
            expiry_date=bankcard.expiry_date,
            amount=amount,
            merchant_reference=order_number,
            ccv=bankcard.ccv,
            shipping_address=shipping_address,
        )

        return self.handle_response(response=response, order_number=order_number, amount=amount)


    def handle_response(self, response, order_number, amount):
        """
        Handle the response sent from the Gateway.
        At this point we have a response from the gateway, here we need to work out what that was.
        :param response:
        :return:
        """
        # Maintain audit trail
        self.record_txn(response, order_number, amount)

        if response.is_successful():
            return response.get_VPSTxId()

        elif response.is_declined():
            msg = self.get_friendly_decline_message()
            raise UnableToTakePayment(msg)

        elif response.is_rejected():
            msg = self.get_friendly_rejected_message()
            raise UnableToTakePayment(msg)

        else:
            msg = self.get_friendly_error_message(response)
            raise UnableToTakePayment(msg)


    def record_txn(self, response, order_number, amount):

        SagePayTransaction.objects.create(
            vendor_tx_code=response.get_VendorTxCode(),
            amount=amount,
            response=response.get_raw_response(),
            )


    def get_friendly_decline_message(self):
        return 'The transaction was declined by your bank - please check your bankcard details and try again.'

    def get_friendly_rejected_message(self):
        return 'The transaction has been rejected or you have had three failed attempts to correctly ' \
               'enter your card details. '

    def get_friendly_error_message(self, response):
        return response.get_status(), response.get_status_message()