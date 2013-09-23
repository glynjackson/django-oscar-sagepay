from django import forms
from oscar.apps.payment.forms import BankcardForm










class CardHolder(forms.CharField):

    def __init__(self, *args, **kwargs):
        _kwargs = {
            'max_length': 80,
            'widget': forms.TextInput(attrs={'autocomplete': 'off'}),
            'label': "Holder Name"
        }
        _kwargs.update(kwargs)
        super(CardHolder, self).__init__(*args, **_kwargs)

    def clean(self, value):
       pass


class SagePayForm(BankcardForm):
    card_holder = CardHolder()


    class Meta(BankcardForm.Meta):

        fields = ('card_holder', 'number', 'start_month', 'expiry_month', 'ccv')
