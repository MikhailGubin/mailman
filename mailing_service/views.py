from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView, UpdateView

from mailing_service.forms import ClientForm, MailingForm, MessageForm
from mailing_service.models import AttemptMailing, Client, Mailing, Message
from mailing_service.services import (CustomCreateView, CustomListView,
                                      MailingService)


class IndexView(ListView):
    """Класс для представления 'Главной страницы'"""

    model = Mailing
    context_object_name = "mailings"
    template_name = "mailing_service/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "clients": Client.objects.all(),
                "launched_mailings": [
                    mailing
                    for mailing in Mailing.objects.all()
                    if mailing.status == "launched"
                ],
                "mailings": Mailing.objects.all(),
            }
        )
        return context


class ClientListView(CustomListView):
    """Класс для представления объектов класса 'Клиент'"""

    model = Client
    context_object_name = "clients"


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Выводит представление отдельного объекта класса 'Клиент'"""

    model = Client
    context_object_name = "client"


class ClientCreateView(CustomCreateView):
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


class MessageListView(CustomListView):
    """Класс для представления объектов класса 'Сообщение'"""

    model = Message
    context_object_name = "messages"


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Выводит представление отдельного объекта класса 'Сообщение'"""

    model = Message
    context_object_name = "message"


class MessageCreateView(CustomCreateView):
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


class MailingListView(CustomListView):
    """Класс для представления объектов класса 'Сообщение'"""

    model = Mailing
    context_object_name = "mailings"


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Выводит представление отдельного объекта класса 'Рассылка'"""

    model = Mailing
    context_object_name = "mailing"


class MailingCreateView(CustomCreateView):
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


class SendMessageView(UpdateView):
    """Отправляет сообщения на почту клиентов"""

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailing_service:mailings_list")
    template_name = "mailing_service/confirm_send_message.html"

    def form_valid(self, form):
        mailing = form.save()
        MailingService.start_mailing(mailing, self.request.user)
        return super().form_valid(form)


@method_decorator(cache_page(60 * 1), name="dispatch")
class AttemptMailingListView(CustomListView):
    """Класс для представления объектов класса 'Попытка рассылки'"""

    model = AttemptMailing
    context_object_name = "attempts"
    template_name = "mailing_service/attempt_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.has_perm("mailing_service.can_view_attempt_mailing"):
            attempts_list = AttemptMailing.objects.all()
        else:
            attempts_list = [
                attempt
                for attempt in AttemptMailing.objects.all()
                if attempt.owner == user
            ]

        context.update(
            {
                "attempts_list": attempts_list,
                "successfully_attempts": [
                    attempt
                    for attempt in attempts_list
                    if attempt.status == "successfully"
                ],
                "unsuccessfully_attempts": [
                    attempt
                    for attempt in attempts_list
                    if attempt.status == "unsuccessfully"
                ],
            }
        )
        return context


class AttemptMailingDetailView(LoginRequiredMixin, DetailView):
    """Выводит представление отдельного объекта класса 'Попытка рассылки'"""

    model = AttemptMailing
    context_object_name = "attempt"
    template_name = "mailing_service/attempt_detail.html"


class MailingCompletedView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing_service:mailings_list")
    template_name = "mailing_service/confirm_mailing_completed.html"

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        if not request.user.has_perm("mailing_service.can_edit_status"):
            return HttpResponseForbidden("У вас нет прав для завершения рассылки.")

        mailing.status = "completed"
        mailing.save()

        return redirect("mailing_service:mailing_detail", pk=pk)
