from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _

from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView
from oscar.apps.payment.models import SourceType, Source
from oscar.apps.payment.forms import BillingAddressForm
from oscar.apps.order.models import ShippingAddress
from oscar.apps.address.models import UserAddress

from .facade import Facade
from .forms import SagePayForm


class SagePayDetailsView(OscarPaymentDetailsView):
    """
    For taking the details of payment and creating the order
    See: https://django-oscar.readthedocs.org/en/latest/ref/apps/checkout.html?highlight=checkout#oscar.apps.checkout.views.PaymentDetailsView
    """

    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        # Add bankcard form to the template context
        ctx = super(SagePayDetailsView, self).get_context_data(**kwargs)
        ctx['bankcard_form'] = kwargs.get('bankcard_form', SagePayForm())

        return ctx


    def post(self, request, *args, **kwargs):
        """
        This method is designed to be overridden by subclasses which will validate the forms from the payment details
        page. If the forms are valid then the method can call submit()
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        if request.POST.get('action', '') == 'place_order':
            return self.do_place_order(request)


        # Check bankcard form is valid
        bankcard_form = SagePayForm(request.POST)
        if not bankcard_form.is_valid():
            ctx = self.get_context_data(**kwargs)
            ctx['bankcard_form'] = bankcard_form
            return self.render_to_response(ctx)

        # Render preview page (with bankcard details hidden)
        return self.render_preview(request, bankcard_form=bankcard_form)


    def do_place_order(self, request):
        bankcard_form = SagePayForm(request.POST)
        if not bankcard_form.is_valid():
            messages.error(request, _("Invalid submission"))
            return HttpResponseRedirect(reverse('checkout:payment-details'))

        bankcard = bankcard_form.bankcard

        # Call oscar's submit method, passing through the bankcard object so it
        # gets passed to the 'handle_payment' method
        return self.submit(request.basket,
                           payment_kwargs={'bankcard': bankcard})


    def handle_payment(self, order_number, total_incl_tax, **kwargs):
        # Make request to SagePay - if there any problems (eg bankcard
        # not valid / request refused by bank) then an exception would be
        # raised and handled)
        facade = Facade()

        sagepay_ref = facade.authorise(
            order_number=order_number,
            amount=total_incl_tax,
            billing_address="122",
            bankcard=kwargs['bankcard'],
            shipping_address=self.get_shipping_address()
        )

        # Request was successful - record the "payment source".
        source_type, _ = SourceType.objects.get_or_create(name='SagePay')

        source = Source(source_type=source_type,
                        currency="GBP",
                        amount_debited=total_incl_tax,
                        reference=sagepay_ref)
        self.add_payment_source(source)

        # Also record payment event
        self.add_payment_event('auth', total_incl_tax)


    # This is only required for Oscar < 0.6 which doesn't support a nice
    # way of getting a ShippingAddress instance without saving it.
    def get_shipping_address(self):
        addr_data = self.checkout_session.new_shipping_address_fields()
        if addr_data:
            return ShippingAddress(**addr_data)

        addr_id = self.checkout_session.user_address_id()
        if addr_id:
            # Create shipping address from an existing user address
            user_addr = UserAddress.objects.get(id=addr_id)
            shipping_addr = ShippingAddress()
            user_addr.populate_alternative_model(shipping_addr)
            return shipping_addr
