from django import forms

from mailing_service.models import Client, Mailing, Message
from mixin_form import StyleFormMixin
from users.models import User


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        exclude = ("owner",)


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        exclude = ("owner",)


class MailingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        exclude = ("finished_at", "status", "owner")


#     def clean_clients(self):
#         clients = self.cleaned_data.get("clients")
#         created_at = self.cleaned_data.get("created_at")
#         for client in clients.values():
#             if not client.get("owner_id") == Mailing:
#                 self.add_error("clients",
#                                f"Нельзя добавлять чужих клиентов в рассылку {created_at}")
#         return clients

# def clean_message(self):
#     message = self.cleaned_data.get("message")
#     if not Mailing.message.owner == Mailing.owner:
#         self.add_error("message",
#                        f"Нельзя добавлять чужие сообщения в рассылку {Mailing.owner, message.owner}")
#     return message Mailing.owner, client
