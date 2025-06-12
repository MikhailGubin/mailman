from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from mailing_service.forms import ClientForm, MessageForm, MailingForm
from mailing_service.models import Client, Message, Mailing


class IndexView(ListView):
    """Класс для представления 'Главной страницы'"""
    model = Mailing
    context_object_name = "mailings"
    template_name = "mailing_service/index.html"

class ClientListView(ListView):
    """Класс для представления объектов класса 'Клиент'"""

    model = Client
    context_object_name = "clients"

class ClientDetailView(LoginRequiredMixin, DetailView):
    """Выводит представление отдельного объекта класса 'Клиент'"""

    model = Client
    context_object_name = "client"


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Создаёт представление объекта класса 'Клиент'"""

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing_service:clients_list")


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Создаёт представление объекта класса 'Клиент'"""

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing_service:clients_list")

    def get_success_url(self):
        """Перенаправляет пользователя на просмотр этого клиента после успешного редактирования записи"""
        return reverse("mailing_service:client_detail", args=[self.kwargs.get("pk")])


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Удаляет представление объекта класса 'Клиент'"""

    model = Client
    success_url = reverse_lazy("mailing_service:clients_list")


class MessageListView(ListView):
    """Класс для представления объектов класса 'Сообщение'"""

    model = Message
    context_object_name = "messages"

class MessageDetailView(LoginRequiredMixin, DetailView):
    """Выводит представление отдельного объекта класса 'Сообщение'"""

    model = Message
    context_object_name = "message"


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создаёт представление объекта класса 'Сообщение'"""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing_service:messages_list")


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Создаёт представление объекта класса 'Сообщение'"""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing_service:messages_list")

    def get_success_url(self):
        """Перенаправляет пользователя на просмотр этого сообщения после успешного редактирования записи"""
        return reverse("mailing_service:message_detail", args=[self.kwargs.get("pk")])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Удаляет представление объекта класса 'Сообщение'"""

    model = Message
    success_url = reverse_lazy("mailing_service:messages_list")


class MailingListView(ListView):
    """Класс для представления объектов класса 'Сообщение'"""

    model = Mailing
    context_object_name = "mailings"

class MailingDetailView(LoginRequiredMixin, DetailView):
    """Выводит представление отдельного объекта класса 'Рассылка'"""

    model = Mailing
    context_object_name = "mailing"


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Создаёт представление объекта класса 'Рассылка'"""

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing_service:mailings_list")


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Создаёт представление объекта класса 'Рассылка'"""

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing_service:mailings_list")

    def get_success_url(self):
        """Перенаправляет пользователя на просмотр этой рассылки после успешного редактирования записи"""
        return reverse("mailing_service:mailing_detail", args=[self.kwargs.get("pk")])


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Удаляет представление объекта класса 'Рассылка'"""

    model = Mailing
    success_url = reverse_lazy("mailing_service:mailings_list")