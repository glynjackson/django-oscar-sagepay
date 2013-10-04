Checkout Mode Banner
=======================

django-oscar-sagepay ships with an optional custom tag that displays a banner dictating
what checkout mode you are running. For example, if you are running in simulator mode
i.e. ``SAGEPAY_MODE = 'Simulator'`` a message banner could be displayed on the payment details view.

===================================
Adding the Checkout Banner
===================================

The banner is not installed by default and is entirely optional. To add the checkout
banner simply add the tage to the required view::

    {% load checkout_mode_tag %}
    {{ bankcard_form.as_table }}


Another example would be to add the custom tag the payment details template::

    {% load checkout_mode_tag %}
    {% block payment_details_content %}
    {% banner %}

    <form action="{% url 'checkout:preview' %}" class="form-stacked" method="POST">
        {% csrf_token %}
        {{ bankcard_form.as_table }}
    </form>
    {% endblock %}

