from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from mailing_service.forms import ClientForm
from mailing_service.models import Client


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
