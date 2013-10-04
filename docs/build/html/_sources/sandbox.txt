Testing in Sandbox
===================

============================
Sandbox Installation
============================

At the time of writing this django-oscar does not have a pip install for version 0.6 or above. Because of this
I have removed django-oscar from the setup.py list of requirements. You will need to first install
Oscar 0.6 directly from github i.e. ``git clone git@github.com:tangentlabs/django-oscar.git``.

To run the plugin in sandbox mode please perform the following steps::

    $ virtualenv django-env
    $ source django-env/bin/activate
    $ make sandbox
    $ sandbox/manage.py runserver
    $ make clean

===================================
SagePay Test Credit Card Numbers
===================================

This is a list of the SagePay test credit card numbers you can use to test transactions
in SagePay Direct when in test and simulator mode.

There are many different test credit card numbers available to use with the SagePay
test server and at each stage you must ensure you enter the numbers and other details required correctly
- failure to do so will return a Not Matched message.


* Visa - 4929000000006
* Visa Delta (Debit) - 4462000000000003
* Visa Electron UK Debit - 4917300000000008
* Mastercard - 5404000000000001
* UK Maestro - 5641820000000005
* International Maestro - 300000000000000004
* American Express - 374200000000004
* Japan Credit Bureau (JCB) - 3569990000000009
* Diners Club - 36000000000008
* Laser Cards - 6304990000000000044

Please note that these Sage Pay test card numbers cannot be used on the live server,
where a real debit or credit card must be used to put through a test transaction.


* Expiry Date: any date in the future
* CV2: 123
* Billing Address: 88 (you only have to use this on the first line)
* Billing Postcode: 412
* 3D Secure Password: password (not used in version 0.1 of django-oscar-sagepay)


