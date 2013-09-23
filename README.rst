SagePay payment gateway package for django-oscar
============

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
-----

git install
in terimal
virtualenv django-env
source django-env/bin/activate
make sandbox
sandbox/manage.py runserver