from django.db import models
from jsonfield import JSONField

# Vendor - Used to authenticate your site.
# This should contain the Sage Pay Vendor Name supplied by Sage Pay when your account was created.

# Currency

# VPSProtocol

class SagePayTransaction(models.Model):

    # Vendor transaction code
    vendor_tx_code = models.CharField(unique=True, max_length=40)
    response = JSONField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.vendor_tx_id

    class Meta:
        app_label = 'sagepay'

