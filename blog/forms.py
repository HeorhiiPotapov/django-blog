from django import forms


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True, label="Ваш Email адресс")
    subject = forms.CharField(required=True, label="Имя")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Сообщение")
