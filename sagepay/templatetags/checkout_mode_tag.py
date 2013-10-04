from classytags.helpers import InclusionTag
from django import template
from django.conf import settings
from django.template.loader import render_to_string


register = template.Library()


class Banner(InclusionTag):
    """
    Displays a checkout mode banner.
    """

    template = 'sagepay/checkout_mode_banner.html'

    def render_tag(self, context, **kwargs):
        template = self.get_template(context, **kwargs)
        if settings.SAGEPAY_MODE == "Live":
            return ''
        data = self.get_context(context, **kwargs)
        return render_to_string(template, data)


register.tag(Banner)