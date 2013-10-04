Installation and Configuration Guide
======================================

-----------------------
Installing Package
-----------------------

To get the latest stable release from PyPi::

    $ pip install django-oscar-sagepay

To get the latest commit from GitHub::

    $ pip install -e git+git://https://github.com/sparky300/django-oscar-sagepay.git#egg=sagepay

Add ``sagepay`` to your ``INSTALLED_APPS``::

     INSTALLED_APPS = (
        ...,
        'sagepay',
        )

Add the ``sagepay`` URLs to your ``urls.py``::

      urlpatterns = patterns('',
        ...
        url(r'^sagepay/', include('sagepay.urls')),
        )

Then migrate your database::

    ./manage.py migrate sagepay

-----------------------
Configuration Settings
-----------------------

In order to test your integration first create a Sage Pay `Simulator Account`_.
Once this has been created you will be given the following...

.. _`Simulator Account`: https://support.sagepay.com/apply/simulator/requestAccount

* Vendor Name
* User Name
* Password


Add the settings from the details you were given::

    SAGEPAY_VENDOR = 'YOUR_VENDOR_NAME'
    SAGEPAY_PASSWORD = 'YOUR_PASSWORD'
    SAGEPAY_CURRENCY = 'GBP'
    SAGEPAY_VPS_PROTOCOL = '2.23'
    # Options are Live, Test and Simulator
    SAGEPAY_MODE = 'Simulator'


Note that both currency and protocol are optional settings, if not set defaults will be used.


--------------------------
Integration into checkout
--------------------------

You'll need to use a subclass of oscar.apps.checkout.views.PaymentDetailsView within your own checkout views.
See Oscar's documentation on how to create a local version of the checkout app.

Once PaymentDetailsView has been added in your checkout view add::


    from sagepay.views import SagePayDetailsView

    class PaymentDetailsView(SagePayDetailsView):
        pass
