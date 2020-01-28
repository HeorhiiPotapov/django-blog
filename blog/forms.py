from django import forms
from django.utils.translation import ugettext_lazy as _


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True, label=_('Your email'))
    subject = forms.CharField(required=True, label=_('Name'))
    message = forms.CharField(widget=forms.Textarea, required=True, label=_('Message'))
