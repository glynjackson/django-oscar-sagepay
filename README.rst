
=================================================
SagePay payment gateway package for django-oscar
=================================================


WARNING THIS PROJECT IS NOT COMPLETE! I'M IN THE PROCESS OF DEVELOPING THIS PLUGIN!
================================================

This package provides integration between django-oscar and the payment gateway SagePay UK

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    $ pip install django-oscar-sagepay

To get the latest commit from GitHub

.. code-block:: bash

    $ pip install -e git+git://https://github.com/sparky300/django-oscar-sagepay.git#egg=sagepay

TODO: Describe further installation steps (edit / remove the examples below):

Add ``sagepay`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'sagepay',
    )

Add the ``sagepay`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^app-url/', include('sagepay.urls')),
    )

Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate sagepay


Configuration
------------

Edit your settings.py to set the following settings:

.. code-block:: bash

    SAGEPAY_VENDOR = 'YOUR_VENDOR_NAME'
    SAGEPAY_PASSWORD = 'YOUR_PASSWORD'
    SAGEPAY_CURRENCY = 'GBP'
    SAGEPAY_VPS_PROTOCOL = '2.23'
    # Options are Live, Test and Simulator
    SAGEPAY_MODE = 'Simulator'


Integration into checkout
-------------------------

You'll need to use a subclass of oscar.apps.checkout.views.PaymentDetailsView within your own checkout views.
See Oscar's documentation on how to create a local version of the checkout app.


Next in your checkout view add the following.


.. code-block:: bash

    from sagepay.views import SagePayDetailsView

    class PaymentDetailsView(SagePayDetailsView):
        pass



Usage
-----

TODO: Describe usage or point to docs. Also describe available settings and
templatetags.


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-oscar-sagepay
    $ python setup.py install
    $ pip install -r dev_requirements.txt

    $ git co -b feature_branch master
    # Implement your feature and tests
    $ git add . && git commit
    $ git push -u origin feature_branch
    # Send us a pull request for your feature branch

Sandbox
-------

To run the plugin in sandbox mode please perform the following steps

.. code-block:: bash

    $ git install
    $ virtualenv django-env
    $ source django-env/bin/activate
    $ make sandbox
    $ sandbox/manage.py runserver