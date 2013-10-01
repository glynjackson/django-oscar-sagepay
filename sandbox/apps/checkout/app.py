from oscar.apps.checkout.app import CheckoutApplication

import views


class OverriddenCheckoutApplication(CheckoutApplication):
    # Specify new view for payment details
    payment_details_view = views.PaymentDetailsView


application = OverriddenCheckoutApplication()