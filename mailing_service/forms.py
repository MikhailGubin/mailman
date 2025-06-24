from django import forms

from mailing_service.models import Client, Mailing, Message
from mixin_form import StyleFormMixin


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        exclude = ("owner",)


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        exclude = ("owner",)


class MailingForm(StyleFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Извлекаем пользователя из kwargs
        super(MailingForm, self).__init__(*args, **kwargs)
        if self.user and "owner" not in self.fields:
            self.instance.owner = self.user
            self.fields['clients'].queryset = Client.objects.filter(owner=self.user)
            self.fields['message'].queryset = Message.objects.filter(owner=self.user)

    class Meta:
        model = Mailing
        exclude = ("finished_at", "status", "owner")
