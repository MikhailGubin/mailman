import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.db import models
from django.views.generic import CreateView, ListView

from config.settings import CACHE_ENABLED, EMAIL_HOST_USER
from mailing_service.models import AttemptMailing


class MailingService:

    @staticmethod
    def start_mailing(mailing, user):
        mailing.start_time = datetime.datetime.now()
        mailing.status = "launched"
        mailing.save()

        title = mailing.message.title
        content = mailing.message.content
        clients = [client.email for client in mailing.clients.all()]

        for client in clients:

            try:
                if "@test.ru" in client:
                    raise Exception("Не правильно указана почта клиента")

                send_mail(
                    subject=title,
                    message=content,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[
                        client,
                    ],
                )

            except Exception as error_text:
                print(str(error_text))
                mailing_attempt = AttemptMailing.objects.create(
                    status="unsuccessfully",
                    server_response=error_text,
                    mailing=mailing,
                    owner=user,
                )

                mailing_attempt.save()
                mailing.finished_at = datetime.datetime.now()
                mailing.status = "completed"
                mailing.save()

            # Если рассылка выполнилась удачно, то выполняется следующий код
            mailing_attempt = AttemptMailing.objects.create(
                status="successfully", mailing=mailing, owner=user
            )
            mailing_attempt.save()

    @staticmethod
    def get_from_cache(queryset, model):
        """Получает данные по продуктам из кэша. Если кэш пуст, получает данные из БД"""
        if not CACHE_ENABLED:
            return queryset
        key = str(model) + "_list"
        objects = cache.get(key)
        if objects is not None:
            return objects
        objects = queryset
        cache.set(key, objects, 60)
        return objects


class CustomCreateView(LoginRequiredMixin, CreateView):
    """Шаблон для создания представления объекта нужного класса"""

    def form_valid(self, form):
        object = form.save()
        user = self.request.user
        object.owner = user
        object.save()
        return super().form_valid(form)


class CustomListView(ListView):
    """Класс для представления объектов нужного класса"""

    model = models.Model

    def get_queryset(self):
        """
        Выводит на экран все объекты, если пользователь является Менеджером.
        В противном случае выводит только те объекты, которые создал данный Пользователь.
        """
        user = self.request.user
        get_queryset = super().get_queryset()
        permissions = [
            user.has_perm("mailing_service.can_view_client"),
            user.has_perm("mailing_service.can_view_message"),
            user.has_perm("mailing_service.can_view_mailing"),
            user.has_perm("mailing_service.can_edit_status"),
            user.has_perm("mailing_service.can_view_attempt_mailing"),
        ]

        if all(permissions):
            return MailingService.get_from_cache(get_queryset, self.model)
        else:
            return MailingService.get_from_cache(
                get_queryset.filter(owner=self.request.user), self.model
            )
