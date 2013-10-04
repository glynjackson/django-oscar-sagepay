from django.test import TestCase


from sagepay.forms import SagePayForm
from sagepay.facade import Facade



class FacadeTests(TestCase):


    def setUp(self):
        self.facade = Facade()
        self.card = SagePayForm('1000350000000007', '10/13', cvv=345)


    def test_authorise(self):

        sagepay_ref = self.facade.authorise(
            order_number="123",
            amount="10.99",
            billing_address="21 Jump Street",
            bankcard=self.card,
            shipping_address="21 Jump Street"
        )

        self.assertTrue(sagepay_ref != "")